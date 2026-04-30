Write-Host "--- Running Aura AI Project Tests ---" -ForegroundColor Cyan

Write-Host ""
Write-Host "[1/2] Running Backend Tests..." -ForegroundColor Yellow
Set-Location backend
pytest
$backendResult = $LASTEXITCODE
Set-Location ..

Write-Host ""
Write-Host "[2/2] Running Frontend Tests..." -ForegroundColor Yellow
Set-Location frontend
npm test -- --watchAll=false
$frontendResult = $LASTEXITCODE
Set-Location ..

Write-Host ""
Write-Host "--- Test Summary ---" -ForegroundColor Cyan

if ($backendResult -eq 0) {
    Write-Host "Backend: PASSED" -ForegroundColor Green
}
else {
    Write-Host "Backend: FAILED" -ForegroundColor Red
}

if ($frontendResult -eq 0) {
    Write-Host "Frontend: PASSED" -ForegroundColor Green
}
else {
    Write-Host "Frontend: FAILED" -ForegroundColor Red
}

if ($backendResult -eq 0 -and $frontendResult -eq 0) {
    Write-Host ""
    Write-Host "All systems check out. Quality assured." -ForegroundColor Green
}
else {
    Write-Host ""
    Write-Host "Some tests failed. Please review the output." -ForegroundColor Red
    exit 1
}
