@echo off
REM ─── Get a timestamp in YYYYMMDD_HHMMSS format ──────────────────────────
for /f "skip=1 tokens=1" %%x in ('wmic os get LocalDateTime') do if not defined LDT set LDT=%%x
set TS=%LDT:~0,8%_%LDT:~8,6%

REM ─── Back up default.swf into old\ with that timestamp ──────────────────
echo Backing up default.swf to old\default_%TS%.swf
copy /Y "default.swf" "old\default_%TS%.swf" >nul

REM ─── Run your JPEXS importScript call ──────────────────────────────────
echo Importing scripts from source\…
"jpexs\ffdec-cli.exe" -importScript "default.swf" "default.swf" "source"

REM ─── Pause so you can see any messages ────────────────────────────────
pause
