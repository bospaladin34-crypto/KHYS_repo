# 1. Launch the 15Hz Sync as a background job (No terminal lock)
Start-Job -Name "SantosHeartbeat" -ScriptBlock {
    $Process = [System.Diagnostics.Process]::GetCurrentProcess()
    $Process.PriorityClass = 'High' 
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    while($true){
        if($sw.ElapsedMilliseconds -ge 66){
            $sw.Restart()
            [System.Threading.Thread]::Sleep(1)
        }
    }
}

# 2. Launch the Visual Dashboard
Start-Process powershell.exe -ArgumentList "-ExecutionPolicy Bypass -File "C:\Sovereign\Siphon_Dashboard.ps1""

Write-Host "--- MANIFOLD RUNNING IN BACKGROUND ---" -ForegroundColor Cyan
Write-Host "The 15Hz Sync is active. Terminal is now FREE for your use." -ForegroundColor Yellow
Write-Host "Type 'Get-Job' to see the heartbeat status." -ForegroundColor White
