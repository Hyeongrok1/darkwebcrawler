import psutil, subprocess
for pid in psutil.pids():
    process = psutil.Process(pid)
    if process.name() == "firefox.exe":
        process.kill()
        
proc = subprocess.Popen(["C:\\Tor Browser\\Browser\\firefox.exe"],
                        stdout = subprocess.PIPE, stderr = subprocess.PIPE)

out, err = proc.communicate()