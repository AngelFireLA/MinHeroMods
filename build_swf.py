"""Build default.swf from the exported and edited Min Hero source tree."""

import csv
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import modified_detector


ROOT = Path(__file__).resolve().parent
SOURCE_FOLDER = ROOT / "source"
IMAGES_FOLDER = SOURCE_FOLDER / "images"
SYMBOLS_FILE = SOURCE_FOLDER / "symbolClass" / "symbols.csv"
ORIGINAL_SWF = ROOT / "original.swf"
OUTPUT_SWF = ROOT / "default.swf"
BACKUP_FOLDER = ROOT / "old"
JPEXS_CLI = ROOT / "jpexs-custom" / "ffdec-cli.jar"
JPEXS_PROFILE = ROOT / ".ffdec-profile"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}
EXPORTED_IMAGE_RE = re.compile(
    r"^(?P<character_id>\d+)_(?P<class_name>.+)\.(?P<extension>png|jpg|jpeg|bmp|webp)$",
    re.IGNORECASE,
)


class BuildError(RuntimeError):
    """Raised when source metadata or a JPEXS command is invalid."""


def run_jpexs(*arguments, capture=False):
    """Run the portable custom JPEXS CLI and fail the build on errors."""
    JPEXS_PROFILE.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    environment["APPDATA"] = str(JPEXS_PROFILE)
    command = ["java", "-jar", str(JPEXS_CLI), *map(str, arguments)]
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=capture,
        env=environment,
    )
    if result.returncode != 0:
        if capture:
            details = "\n".join(
                part.strip() for part in (result.stdout, result.stderr) if part.strip()
            )
            raise BuildError(details or f"JPEXS exited with code {result.returncode}")
        raise BuildError(f"JPEXS exited with code {result.returncode}: {' '.join(command)}")
    return result


def load_symbols():
    """Return SymbolClass rows and validate their character IDs."""
    rows = []
    with SYMBOLS_FILE.open(newline="", encoding="utf-8-sig") as source:
        for row in csv.reader(source, delimiter=";"):
            if not row:
                continue
            if len(row) != 2 or not row[0].isdigit():
                raise BuildError(f"Invalid SymbolClass row: {row}")
            rows.append((int(row[0]), row[1]))
    return rows


def save_symbols(rows):
    """Write deterministic SymbolClass metadata."""
    with SYMBOLS_FILE.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.writer(destination, delimiter=";", lineterminator="\n")
        writer.writerows(rows)


def safe_class_suffix(stem):
    """Convert an arbitrary Min Hero image stem into an AS3 identifier suffix."""
    suffix = re.sub(r"[^A-Za-z0-9_$]", "_", stem)
    if not suffix or not re.match(r"[A-Za-z_$]", suffix):
        suffix = f"image_{suffix}"
    return suffix


def ensure_sprite_handler_source(class_name, image_name):
    """Create the Min Hero BitmapAsset wrapper for a new SpriteHandler image."""
    prefix = "Utilities.SpriteHandler_"
    if not class_name.startswith(prefix):
        return

    suffix = class_name[len(prefix):]
    class_simple_name = f"SpriteHandler_{suffix}"
    wrapper_path = SOURCE_FOLDER / "scripts" / "Utilities" / f"{class_simple_name}.as"
    if not wrapper_path.exists():
        wrapper_path.write_text(
            "package Utilities\n"
            "{\n"
            "   import mx.core.BitmapAsset;\n\n"
            f'   [Embed(source="/_assets/{image_name}")]\n'
            f"   public class {class_simple_name} extends BitmapAsset\n"
            "   {\n"
            f"      public function {class_simple_name}()\n"
            "      {\n"
            "         super();\n"
            "      }\n"
            "   }\n"
            "}\n",
            encoding="utf-8",
        )
        print(f"Created image wrapper: {wrapper_path.relative_to(SOURCE_FOLDER)}")
    else:
        wrapper_source = wrapper_path.read_text(encoding="utf-8")
        embed_pattern = re.compile(r'\[Embed\(source="/_assets/[^"\r\n]+"\)\]')
        expected_embed = f'[Embed(source="/_assets/{image_name}")]'
        if expected_embed not in wrapper_source:
            if not embed_pattern.search(wrapper_source):
                raise BuildError(f"Cannot find Embed metadata in {wrapper_path}")
            wrapper_source = embed_pattern.sub(expected_embed, wrapper_source, count=1)
            wrapper_path.write_text(wrapper_source, encoding="utf-8")
            print(f"Updated image wrapper: {wrapper_path.relative_to(SOURCE_FOLDER)}")

    main_handler_path = SOURCE_FOLDER / "scripts" / "Utilities" / "SpriteHandler.as"
    main_handler_source = main_handler_path.read_text(encoding="utf-8")
    registration = f"      private static var {suffix}:Class = {class_simple_name};"
    if registration not in main_handler_source:
        marker = "   public class SpriteHandler"
        marker_index = main_handler_source.find(marker)
        if marker_index < 0:
            raise BuildError(f"Cannot find SpriteHandler class in {main_handler_path}")
        opening_brace_index = main_handler_source.find("{", marker_index)
        if opening_brace_index < 0:
            raise BuildError(f"Cannot find SpriteHandler class body in {main_handler_path}")
        insert_index = opening_brace_index + 1
        main_handler_source = (
            main_handler_source[:insert_index]
            + "\n"
            + registration
            + main_handler_source[insert_index:]
        )
        main_handler_path.write_text(main_handler_source, encoding="utf-8")
        print(f"Registered image wrapper in {main_handler_path.relative_to(SOURCE_FOLDER)}")


def normalize_new_images():
    """Rename only new Min Hero images and synchronize symbols.csv."""
    baseline = modified_detector.load_previous_hashes()
    symbols = load_symbols()
    ids_in_use = {character_id for character_id, _ in symbols}
    next_character_id = max(ids_in_use, default=0) + 1
    changed_symbols = False

    for image_path in sorted(IMAGES_FOLDER.iterdir(), key=lambda path: path.name.lower()):
        if not image_path.is_file() or image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        if image_path.name.lower().endswith(".alpha.png"):
            continue

        relative_path = image_path.relative_to(SOURCE_FOLDER).as_posix()
        if relative_path in baseline:
            continue

        match = EXPORTED_IMAGE_RE.match(image_path.name)
        if match:
            character_id = int(match.group("character_id"))
            class_name = match.group("class_name")
        else:
            while next_character_id in ids_in_use:
                next_character_id += 1
            character_id = next_character_id
            next_character_id += 1
            class_name = f"Utilities.SpriteHandler_{safe_class_suffix(image_path.stem)}"
            renamed_path = image_path.with_name(
                f"{character_id}_{class_name}{image_path.suffix.lower()}"
            )
            if renamed_path.exists():
                raise BuildError(f"Cannot rename image; destination exists: {renamed_path}")
            image_path.rename(renamed_path)
            print(f"Renamed new image: {image_path.name} -> {renamed_path.name}")
            image_path = renamed_path

        existing_id_class = next(
            (existing_class for existing_id, existing_class in symbols if existing_id == character_id),
            None,
        )
        if existing_id_class is not None and existing_id_class != class_name:
            raise BuildError(
                f"Image character ID {character_id} is already assigned to {existing_id_class}."
            )
        existing_class_id = next(
            (existing_id for existing_id, existing_class in symbols if existing_class == class_name),
            None,
        )
        if existing_class_id is not None and existing_class_id != character_id:
            raise BuildError(
                f"Image class {class_name} is already assigned to character {existing_class_id}."
            )
        if existing_id_class is None and existing_class_id is None:
            symbols.append((character_id, class_name))
            changed_symbols = True
        ids_in_use.add(character_id)
        ensure_sprite_handler_source(class_name, image_path.name)

    if changed_symbols:
        save_symbols(symbols)


def parse_new_image(path):
    """Read character and class metadata from a normalized image filename."""
    match = EXPORTED_IMAGE_RE.match(path.name)
    if not match:
        raise BuildError(f"New image does not follow the normalized naming style: {path}")
    return int(match.group("character_id")), match.group("class_name")


def add_new_scripts_with_retries(script_paths, working_swf, temp_folder):
    """Retry scripts so simple dependencies between new classes can resolve."""
    pending = list(script_paths)
    last_errors = {}
    output_index = 0
    while pending:
        made_progress = False
        for script_path in pending[:]:
            candidate_swf = temp_folder / f"added_script_{output_index}.swf"
            output_index += 1
            try:
                run_jpexs(
                    "-addScript",
                    script_path,
                    working_swf,
                    candidate_swf,
                    capture=True,
                )
            except BuildError as error:
                last_errors[script_path] = str(error)
                continue
            working_swf = candidate_swf
            print(f"Added new script: {script_path.relative_to(SOURCE_FOLDER)}")
            pending.remove(script_path)
            made_progress = True
        if not made_progress:
            details = "\n\n".join(
                f"{path}:\n{last_errors.get(path, 'unknown compilation error')}"
                for path in pending
            )
            raise BuildError(f"Could not compile new AS3 scripts:\n{details}")
    return working_swf


def backup_current_output():
    """Keep the previous playable SWF before replacing it."""
    if not OUTPUT_SWF.exists():
        return
    BACKUP_FOLDER.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_FOLDER / f"default_{timestamp}.swf"
    shutil.copy2(OUTPUT_SWF, backup_path)
    print(f"Backed up default.swf to {backup_path.relative_to(ROOT)}")


def cleanup_abandoned_build_folders():
    """Remove work folders left by an interrupted or killed earlier build."""
    root = ROOT.resolve()
    for folder in ROOT.glob("minhero_build_*"):
        resolved = folder.resolve()
        if not folder.is_dir() or resolved.parent != root:
            continue
        try:
            shutil.rmtree(resolved)
            print(f"Removed abandoned build folder: {folder.name}")
        except OSError as error:
            print(
                f"Warning: could not remove abandoned build folder {folder.name}: {error}",
                file=sys.stderr,
            )


def main():
    """Build a fresh SWF from original.swf and all detected source changes."""
    if not JPEXS_CLI.is_file():
        raise BuildError(f"Custom JPEXS CLI is missing: {JPEXS_CLI}")
    if not ORIGINAL_SWF.is_file():
        raise BuildError(f"Base SWF is missing: {ORIGINAL_SWF}")
    if not SYMBOLS_FILE.is_file():
        raise BuildError(f"SymbolClass file is missing: {SYMBOLS_FILE}")

    cleanup_abandoned_build_folders()
    normalize_new_images()
    changes = modified_detector.main()
    new_scripts = [
        SOURCE_FOLDER / change["path"]
        for change in changes
        if change["status"] == "new"
        and change["path"].startswith("scripts/")
        and change["path"].lower().endswith(".as")
    ]
    new_images = [
        SOURCE_FOLDER / change["path"]
        for change in changes
        if change["status"] == "new"
        and change["path"].startswith("images/")
        and Path(change["path"]).suffix.lower() in IMAGE_EXTENSIONS
        and not change["path"].lower().endswith(".alpha.png")
    ]

    backup_current_output()
    with tempfile.TemporaryDirectory(
        prefix="minhero_build_", dir=ROOT, ignore_cleanup_errors=True
    ) as temp_folder:
        temp_folder = Path(temp_folder)
        working_swf = temp_folder / "working.swf"
        scripts_swf = temp_folder / "scripts.swf"
        images_swf = temp_folder / "images.swf"
        final_swf = temp_folder / "final.swf"
        shutil.copy2(ORIGINAL_SWF, working_swf)

        asset_swf = working_swf
        for image_index, image_path in enumerate(new_images):
            character_id, class_name = parse_new_image(image_path)
            image_output_swf = temp_folder / f"added_image_{image_index}.swf"
            run_jpexs(
                "-addImage",
                "-characterId",
                character_id,
                "-class",
                class_name,
                image_path,
                asset_swf,
                image_output_swf,
            )
            asset_swf = image_output_swf
            print(f"Added new image: {image_path.relative_to(SOURCE_FOLDER)}")

        asset_swf = add_new_scripts_with_retries(new_scripts, asset_swf, temp_folder)
        run_jpexs("-importScript", asset_swf, scripts_swf, ROOT / "modified")
        run_jpexs("-importImages", scripts_swf, images_swf, ROOT / "modified")

        # Do not round-trip the exported symbols.csv here. Min Hero has multiple
        # SymbolClass tags/timelines that legitimately reuse character IDs. In
        # particular, ID 5 is Preloader_LOADER_FONT in the preloader and
        # Utilities.SpriteHandler_MAIN_FONT in the main timeline. JPEXS's flat
        # CSV importer applies the last ID mapping to both tags, which makes the
        # preloader throw Error #1065 before the main SpriteHandler ABC loads.
        # -addImage -class above already registers every newly added image.
        shutil.copy2(images_swf, OUTPUT_SWF)

    print(f"Build completed: {OUTPUT_SWF}")


if __name__ == "__main__":
    try:
        main()
    except (BuildError, OSError) as error:
        print(f"Build failed: {error}", file=sys.stderr)
        raise SystemExit(1)
