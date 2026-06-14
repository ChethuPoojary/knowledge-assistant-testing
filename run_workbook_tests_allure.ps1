$ErrorActionPreference = "Continue"

$sheets = @(
    "1_HappyPath",
    "2_Lifecycle",
    "3_RoleBoundary",
    "4_RegionBoundary",
    "5_Citation",
    "6_Hallucination",
    "7_Security",
    "8_EdgeCases",
    "9_CrossRegion",
    "10_APIvsUI"
)

python -m pip install -r requirements.txt
python -m playwright install chromium
python scripts/analyze_testsuite.py

New-Item -ItemType Directory -Force -Path "reports\junit" | Out-Null
New-Item -ItemType Directory -Force -Path "reports\allure-results-by-sheet" | Out-Null
New-Item -ItemType Directory -Force -Path "reports\allure-reports-by-sheet" | Out-Null

foreach ($sheet in $sheets) {
    $safeSheet = ($sheet -replace '[^A-Za-z0-9_.-]', '_')
    $resultsDir = "reports\allure-results-by-sheet\$safeSheet"
    $reportDir = "reports\allure-reports-by-sheet\$safeSheet"
    $junitFile = "reports\junit\$safeSheet.xml"

    Write-Host ""
    Write-Host "==== Running sheet: $sheet ===="
    Remove-Item -LiteralPath $resultsDir -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Force -Path $resultsDir | Out-Null

    python -m pytest tests_generated -v --sheet "$sheet" --alluredir "$resultsDir" --junitxml "$junitFile"

    if (Get-Command allure.cmd -ErrorAction SilentlyContinue) {
        allure.cmd generate "$resultsDir" --clean --single-file --name "$sheet Execution Report - Chethan Poojary" -o "$reportDir"
    }
    elseif (Get-Command allure -ErrorAction SilentlyContinue) {
        allure generate "$resultsDir" --clean --single-file --name "$sheet Execution Report - Chethan Poojary" -o "$reportDir"
    }
    else {
        Write-Warning "Allure CLI is not installed. Raw results are available at $resultsDir"
    }
}

python scripts/build_consolidated_summary.py

Write-Host ""
Write-Host "All sheet reports:"
Write-Host "reports\allure-reports-by-sheet"
Write-Host ""
Write-Host "Consolidated summary:"
Write-Host "reports\consolidated_execution_summary.md"
Write-Host ""
Write-Host "Open a sheet report with:"
Write-Host "reports\allure-reports-by-sheet\1_HappyPath\index.html"
