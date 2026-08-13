# scripts/check.ps1 — run before every commit
Write-Host "Checking architecture boundaries..." -ForegroundColor Cyan
lint-imports
if ($LASTEXITCODE -ne 0) {
    Write-Host "Architecture check FAILED. Fix the import above before committing." -ForegroundColor Red
    exit 1
}
Write-Host "Architecture check passed." -ForegroundColor Green