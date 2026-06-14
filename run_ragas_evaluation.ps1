$ErrorActionPreference = "Stop"

$outputDir = "reports\ragas-evaluation"

Write-Host "Installing RAGAS evaluation dependencies..."
python -m pip install -r requirements.txt

Write-Host "Checking RAGAS setup..."
python .\check_ragas_setup.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "RAGAS setup check failed. Fix the message above and run again."
}

Write-Host "Cleaning previous RAG evaluation report..."
Remove-Item -LiteralPath $outputDir -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

Write-Host "Running RAGAS evaluation pipeline..."
python .\run_ragas_evaluation.py --output-dir $outputDir

Write-Host ""
Write-Host "RAG evaluation report:"
Write-Host "$outputDir\index.html"
