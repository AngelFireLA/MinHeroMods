@echo off

REM 1) Run the Python diff-and-copy script
echo == Checking for modified .as files ==
python modified_detector.py

REM 2) Backup your default.swf with a timestamp
for /f "skip=1 tokens=1" %%x in ('wmic os get LocalDateTime') do if not defined LDT set LDT=%%x
set TS=%LDT:~0,8%_%LDT:~8,6%
echo Backing up default.swf → old\default_%TS%.swf
copy /Y "default.swf" "old\default_%TS%.swf" >nul

REM ─── Run your JPEXS importScript call ──────────────────────────────────
echo Importing scripts from modified\…
"jpexs\ffdec-cli.exe" -importScript "original.swf" "default.swf" "modified"

pause
