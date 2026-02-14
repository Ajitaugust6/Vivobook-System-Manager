import psutil
import subprocess
import platform
import re

# --- 1. SYSTEM MONITOR (CPU & RAM) ---
class SystemMonitor:
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=0)

    def get_ram_usage(self):
        ram = psutil.virtual_memory()
        return {
            "percent": ram.percent,
            "used_gb": round(ram.used / (1024**3), 2),
            "total_gb": round(ram.total / (1024**3), 2)
        }

# --- 2. POWER CONTROLLER (Gaming Mode) ---
class PowerController:
    def set_high_performance(self):
        # GUID for High Performance
        try:
            subprocess.run(["powercfg", "/setactive", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"], check=True)
            return "Active: High Performance"
        except:
            return "Error: Permission Denied"

    def set_balanced(self):
        # GUID for Balanced
        try:
            subprocess.run(["powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"], check=True)
            return "Active: Balanced Mode"
        except:
            return "Error: Permission Denied"

# --- 3. MEMORY OPTIMIZER (The Cleaner) ---
class MemoryOptimizer:
    def __init__(self):
        self.bloatware = [
            "chrome.exe", "msedge.exe", "discord.exe", "spotify.exe", 
            "teams.exe", "calculator.exe", "phoneexperiencehost.exe", 
            "widgets.exe", "steamwebhelper.exe"
        ]

    def purge_bloatware(self):
        killed_count = 0
        freed_mb = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                if proc.info['name'].lower() in self.bloatware:
                    mem = proc.info['memory_info'].rss / (1024 * 1024)
                    psutil.Process(proc.info['pid']).terminate()
                    killed_count += 1
                    freed_mb += mem
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return killed_count, round(freed_mb, 2)

# --- 4. NETWORK MONITOR (The Ping Tracker) ---
class NetworkMonitor:
    def get_ping(self, host="8.8.8.8"):
        # Returns integer latency in ms, or 999 if timed out
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', '-w', '1000', host] # Wait max 1s
        
        try:
            # Hide the command window popup
            if platform.system().lower() == 'windows':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                output = subprocess.check_output(command, startupinfo=startupinfo).decode()
            else:
                output = subprocess.check_output(command).decode()

            # Parse "time=24ms"
            if "time=" in output:
                # Regex to find the number before 'ms'
                match = re.search(r'time=(\d+)ms', output)
                if match:
                    return int(match.group(1))
            return 999
        except:
            return 999