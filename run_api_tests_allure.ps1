$ErrorActionPreference = "Stop"

$resultsDir = "reports/allure-results"
$reportDir = "reports/allure-report"
$junitFile = "reports/api-test-results.xml"
$reportName = "API Execution Report - Chethan Poojary"

Remove-Item -Recurse -Force $resultsDir, $reportDir -ErrorAction SilentlyContinue
Remove-Item -Force $junitFile -ErrorAction SilentlyContinue

python -m pip install -r requirements.txt
$testExitCode = 0
pytest api-tests -v --alluredir=$resultsDir --junitxml=$junitFile
if ($LASTEXITCODE -ne 0) {
    $testExitCode = $LASTEXITCODE
}

@"
Report=API Execution Report
Author=Chethan Poojary
Owner=Chethan Poojary
Tester=Chethan Poojary
Automation Engineer=Chethan Poojary
Execution Layer=API
Project=Knowledge Assistant
"@ | Set-Content -Path "$resultsDir/environment.properties" -Encoding UTF8

if (Get-Command allure.cmd -ErrorAction SilentlyContinue) {
    allure.cmd generate $resultsDir --clean --single-file --name $reportName -o $reportDir
}
elseif (Get-Command allure -ErrorAction SilentlyContinue) {
    allure generate $resultsDir --clean --single-file --name $reportName -o $reportDir
}
else {
    Write-Warning "Allure CLI is not installed. Raw Allure results were still created."
}

Write-Host ""
Write-Host "Allure raw results: $resultsDir"
Write-Host "Allure single-file report: $reportDir/index.html"
Write-Host "JUnit report: $junitFile"
Write-Host ""
Write-Host "Double-click this report from File Explorer: $reportDir/index.html"

exit $testExitCode
