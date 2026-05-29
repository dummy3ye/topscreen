@echo on
echo Building topscreen...
go build -o topscreen.exe ./cmd/topscreen
if %ERRORLEVEL% EQU 0 (
    echo Build successful: topscreen.exe
) else (
    echo Build failed.
)
