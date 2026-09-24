$uv = "C:\Users\Daniel\.local\bin\uv.exe"

Write-Host "=== pytest ===" -ForegroundColor Cyan
& $uv run pytest
$pytestCode = $LASTEXITCODE

Write-Host "`n=== ruff ===" -ForegroundColor Cyan
& $uv run ruff check .
$ruffCode = $LASTEXITCODE

Write-Host "`n=== pyright ===" -ForegroundColor Cyan
& $uv run pyright
$pyrightCode = $LASTEXITCODE

Write-Host "`n=== summary ===" -ForegroundColor Cyan
Write-Host "pytest : $pytestCode (5 = no tests yet, that's fine for now)"
Write-Host "ruff   : $ruffCode (0 = clean)"
Write-Host "pyright: $pyrightCode (0 = clean)"
