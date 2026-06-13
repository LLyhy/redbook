# 红宝书本地模型一键安装脚本
# 双击运行，自动安装 Ollama + 下载模型 + 创建红宝书

$ErrorActionPreference = "Stop"
Write-Host "`n========================================" -ForegroundColor Red
Write-Host "  红宝书 本地 AI 一键安装" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Red

# Step 1: Check/install Ollama
Write-Host "[1/4] Checking Ollama..." -ForegroundColor Yellow
$ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
if (-not (Test-Path $ollamaPath)) {
    Write-Host "  Downloading Ollama installer..." -ForegroundColor Gray
    $installer = "$env:TEMP\OllamaSetup.exe"
    Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile $installer -UseBasicParsing
    Write-Host "  Installing Ollama (this will take a moment)..." -ForegroundColor Gray
    Start-Process -FilePath $installer -ArgumentList "/S" -Wait
    Remove-Item $installer -Force
    Write-Host "  Ollama installed!" -ForegroundColor Green
} else {
    Write-Host "  Ollama already installed" -ForegroundColor Green
}

# Start Ollama if not running
$ollamaRunning = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
if (-not $ollamaRunning) {
    Write-Host "  Starting Ollama..." -ForegroundColor Gray
    Start-Process -FilePath $ollamaPath -WindowStyle Hidden
    Start-Sleep -Seconds 3
}

# Step 2: Check model
Write-Host "`n[2/4] Checking model..." -ForegroundColor Yellow
$modelList = & $ollamaPath list 2>&1
if ($modelList -match "qwen2.5:3b") {
    Write-Host "  qwen2.5:3b already downloaded" -ForegroundColor Green
} else {
    Write-Host "  Downloading qwen2.5:3b (about 2GB, this will take 5-10 minutes)..." -ForegroundColor Gray
    & $ollamaPath pull qwen2.5:3b
    Write-Host "  Model downloaded!" -ForegroundColor Green
}

# Step 3: Create redbook model
Write-Host "`n[3/4] Creating redbook model..." -ForegroundColor Yellow
$modelfilePath = Join-Path $PSScriptRoot "Modelfile"
if (-not (Test-Path $modelfilePath)) {
    Write-Host "  ERROR: Modelfile not found at $modelfilePath" -ForegroundColor Red
    exit 1
}
$rbList = & $ollamaPath list 2>&1
if ($rbList -match "redbook") {
    Write-Host "  redbook model exists, recreating..." -ForegroundColor Gray
    & $ollamaPath rm redbook 2>$null
}
Push-Location $PSScriptRoot
& $ollamaPath create redbook -f Modelfile
Pop-Location
Write-Host "  redbook model created!" -ForegroundColor Green

# Step 4: Test
Write-Host "`n[4/4] Testing redbook model..." -ForegroundColor Yellow
Write-Host "  Ask: 分析一下两数之和" -ForegroundColor Gray
$result = & $ollamaPath run redbook "分析一下两数之和" 2>&1
Write-Host "`n  Reply preview:" -ForegroundColor Cyan
Write-Host $result.Substring(0, [Math]::Min(300, $result.Length)) -ForegroundColor White

Write-Host "`n========================================" -ForegroundColor Red
Write-Host "  安装完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Red
Write-Host "`n  使用方法:" -ForegroundColor White
Write-Host "    ollama run redbook" -ForegroundColor Gray
Write-Host "    输入问题，红宝书直接回答" -ForegroundColor Gray
Write-Host "`n  或者打开聊天页面:"
Write-Host "    https://llyhy.github.io/redbook/chat/" -ForegroundColor Gray
Write-Host "    在设置里选「本地红宝书」" -ForegroundColor Gray
Write-Host ""

Read-Host "按 Enter 退出"