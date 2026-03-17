while($true){ $sw = [System.Diagnostics.Stopwatch]::StartNew(); while($sw.ElapsedMilliseconds -lt 66){}; $sw.Restart(); [System.Threading.Thread]::Sleep(1) }
