@echo off

REM 1) Run the Python diff-and-copy script
echo == Checking for modified .as files ==
python modified_detector.py

REM ─── Run your JPEXS importScript call ──────────────────────────────────
echo Importing scripts from modified\…
"jpexs\ffdec-cli.exe" -importScript "original.swf" "default.swf" "modified"

pause
