# req.ps1 - Dependency checker for topscreen

function Check-Command {
    param([string]$Name, [string]$Description)
    $path = Get-Command $Name -ErrorAction SilentlyContinue
    if ($path) {
        Write-Host "[OK] $Description ($Name) found at: $($path.Source)" -ForegroundColor Green
        return $true
    } else {
        Write-Host "[MISSING] $Description ($Name) not found in PATH." -ForegroundColor Red
        return $false
    }
}

Write-Host "--- topscreen Dependency Check ---" -Style Bold

$allOk = $true

# 1. Check Go
if (-not (Check-Command "go" "Go Language")) { $allOk = $false }

# 2. Check C Compiler (Required for Fyne/Cgo)
if (-not (Check-Command "gcc" "C Compiler (GCC/MinGW)")) { 
    Write-Host "     Note: Fyne requires a C compiler on Windows for its first build." -ForegroundColor Yellow
    $allOk = $false 
}

# 3. Check ADB
if (-not (Check-Command "adb" "Android Debug Bridge (ADB)")) { $allOk = $false }

# 4. Check scrcpy (Optional but recommended)
Check-Command "scrcpy" "scrcpy Mirroring Tool" | Out-Null

Write-Host "`n--- Go Modules Check ---"
if (Test-Path "go.mod") {
    Write-Host "[OK] go.mod found." -ForegroundColor Green
} else {
    Write-Host "[ERROR] go.mod not found. Run 'go mod init topscreen' in root." -ForegroundColor Red
    $allOk = $false
}

Write-Host "`n--- Summary ---"
if ($allOk) {
    Write-Host "Environment looks good! If the build is slow, it's likely Fyne compiling Cgo for the first time." -ForegroundColor Cyan
} else {
    Write-Host "Some dependencies are missing. Please install them to ensure a successful build." -ForegroundColor Red
}
