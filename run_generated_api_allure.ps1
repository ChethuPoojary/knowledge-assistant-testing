$ErrorActionPreference = "Continue"

$resultsDir = "reports\allure-results-api"
$reportDir = "reports\allure-report-api"
$junitFile = "reports\api-results.xml"
$reportName = "API Execution Report - Chethan Poojary"

Write-Host "Cleaning old API reports..."
Remove-Item -Recurse -Force $resultsDir, $reportDir -ErrorAction SilentlyContinue
Remove-Item -Force $junitFile -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path "reports" | Out-Null

Write-Host "Installing required dependencies..."
python -m pip install -r requirements.txt

Write-Host "Executing generated API tests..."
$testExitCode = 0
python -m pytest tests_generated\test_api_from_workbook.py -v --alluredir=$resultsDir --junitxml=$junitFile
if ($LASTEXITCODE -ne 0) {
    $testExitCode = $LASTEXITCODE
}

Write-Host "Adding Allure environment metadata..."
@"
Report=API Execution Report
Author=Chethan Poojary
Owner=Chethan Poojary
Tester=Chethan Poojary
Automation Engineer=Chethan Poojary
Execution Layer=API
Project=Knowledge Assistant
"@ | Set-Content -Path "$resultsDir\environment.properties" -Encoding UTF8

Write-Host "Generating single-file Allure report that can be opened directly from folder..."
allure.cmd generate $resultsDir --clean --single-file --name $reportName -o $reportDir

Write-Host ""
Write-Host "Direct-open report file:"
Write-Host "$reportDir\index.html"
Write-Host "You can double-click this index.html from File Explorer."
Write-Host ""

exit $testExitCode
