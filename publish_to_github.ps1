param(
    [string]$RepoUrl = "https://github.com/ChethuPoojary/knowledge-assistant-testing.git"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is not installed or not available on PATH. Install Git for Windows, then run this script again."
}

if (-not (Test-Path -LiteralPath ".git")) {
    git init -b main
}

git add .
git commit -m "Initial QA assignment submission"

$existingRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($existingRemote)) {
    git remote add origin $RepoUrl
}
else {
    git remote set-url origin $RepoUrl
}

git push -u origin main

