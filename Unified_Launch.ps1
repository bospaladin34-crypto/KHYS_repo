# Set Priority to High for the entire session
[System.Diagnostics.Process]::GetCurrentProcess().PriorityClass = 'High'

# Start the Background Sync Job
Start-Job -Name "SantosHeartbeat" -ScriptBlock {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    while($true){
        if($sw.ElapsedMilliseconds -ge 66){
            $sw.Restart()
            [System.Threading.Thread]::Sleep(1)
        }
    }
}

# Launch the Dashboard logic directly
powershell.exe -ExecutionPolicy Bypass -File "C:\Sovereign\Siphon_Dashboard.ps1"
