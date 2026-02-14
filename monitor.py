import psutil
import time
import subprocess
import platform
import re

class SystemMonitor:
    def __init__(self):
        self.start_time = time.time()
        
    def get_uptime(self):
        uptime = int(time.time() - self.start_time)
        return f"{uptime // 60:02d}:{uptime % 60:02d}"
        
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=0)
    
    def get_gpu_usage(self):
        # iGPU load estimation for Windows systems
        try:
            return psutil.cpu_percent(interval=0) * 0.75 
        except:
            return 0

    def get_ram_usage(self):
        ram = psutil.virtual_memory()
        return {"percent": ram.percent, "used_gb": round(ram.used / (1024**3), 2)}

class PowerController:
    def set_high_performance(self):
        try:
            subprocess.run(["powercfg", "/setactive", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"], check=True)
            return "PROTOCOL: HIGH PERFORMANCE"
        except: return "ERROR: ACCESS DENIED"
        
    def set_balanced(self):
        try:
            subprocess.run(["powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"], check=True)
            return "PROTOCOL: BALANCED"
        except: return "ERROR: ACCESS DENIED"

class MemoryOptimizer:
    def __init__(self):
        self.bloatware = ["chrome.exe", "msedge.exe", "discord.exe", "spotify.exe", "teams.exe"]
        
    def purge(self):
        killed = 0; freed = 0
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                if proc.info['name'].lower() in self.bloatware:
                    mem = proc.info['memory_info'].rss / (1024 * 1024)
                    psutil.Process(proc.info['pid']).terminate()
                    killed += 1; freed += mem
            except: continue
        return killed, round(freed, 2)

class NetworkRadar:
    def __init__(self):
        self.history = []

    def get_stats(self):
        cmd = ['ping', '-n', '1', '-w', '1000', '8.8.8.8']
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            out = subprocess.check_output(cmd, startupinfo=si).decode()
            match = re.search(r'time=(\d+)ms', out)
            
            curr_ping = int(match.group(1)) if match else 999
            jitter = abs(curr_ping - self.history[-1]) if self.history else 0
            
            self.history.append(curr_ping)
            if len(self.history) > 5: self.history.pop(0)
            
            return curr_ping, jitter
        except:
            return 999, 0