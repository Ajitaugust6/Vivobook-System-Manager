import customtkinter as ctk
import threading
import time
from monitor import SystemMonitor, PowerController, MemoryOptimizer, NetworkMonitor

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Latency Assassin v3.0 (Threaded)")
        self.geometry("500x600")
        self.resizable(False, False)

        # Initialize Backend Tools
        self.monitor = SystemMonitor()
        self.power = PowerController()
        self.optimizer = MemoryOptimizer()
        self.net_monitor = NetworkMonitor()

        # Shared Variables for Threading
        self.current_ping = 0
        self.ping_status_color = "gray"
        self.running = True # To stop threads when app closes

        # --- UI LAYOUT ---
        
        # 1. Header
        self.lbl_title = ctk.CTkLabel(self, text="SYSTEM COMMANDER", font=("Impact", 28))
        self.lbl_title.pack(pady=20)

        # 2. CPU / RAM Section
        self.frame_stats = ctk.CTkFrame(self)
        self.frame_stats.pack(pady=10, padx=20, fill="x")
        
        self.lbl_cpu = ctk.CTkLabel(self.frame_stats, text="CPU Usage: --%", font=("Arial", 14, "bold"))
        self.lbl_cpu.pack(pady=5)
        self.prog_cpu = ctk.CTkProgressBar(self.frame_stats, width=350)
        self.prog_cpu.pack(pady=5)

        self.lbl_ram = ctk.CTkLabel(self.frame_stats, text="RAM Usage: --%", font=("Arial", 14, "bold"))
        self.lbl_ram.pack(pady=5)
        self.prog_ram = ctk.CTkProgressBar(self.frame_stats, width=350, progress_color="#1f6aa5")
        self.prog_ram.pack(pady=5)

        # 3. Network Radar (Ping)
        self.frame_net = ctk.CTkFrame(self)
        self.frame_net.pack(pady=10, padx=20, fill="x")

        self.lbl_net_header = ctk.CTkLabel(self.frame_net, text="NETWORK LATENCY (Google DNS)", font=("Arial", 12))
        self.lbl_net_header.pack(pady=5)

        self.lbl_ping = ctk.CTkLabel(self.frame_net, text="Ping: -- ms", font=("Arial", 30, "bold"))
        self.lbl_ping.pack(pady=5)
        
        self.lbl_net_status = ctk.CTkLabel(self.frame_net, text="Initializing Radar...", font=("Arial", 12))
        self.lbl_net_status.pack(pady=5)

        # 4. Controls (Power & Purge)
        self.frame_controls = ctk.CTkFrame(self)
        self.frame_controls.pack(pady=20, padx=20, fill="x")

        # Power Switch
        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(
            self.frame_controls, 
            text="GAMING MODE (High Perf)", 
            command=self.toggle_mode,
            variable=self.switch_var, 
            onvalue="on", 
            offvalue="off",
            font=("Arial", 14)
        )
        self.switch.pack(pady=15)

        # Purge Button
        self.btn_purge = ctk.CTkButton(
            self.frame_controls, 
            text="PURGE BLOATWARE (Kill Background Apps)", 
            fg_color="#D43636", 
            hover_color="#8B0000",
            height=40,
            font=("Arial", 12, "bold"),
            command=self.run_purge
        )
        self.btn_purge.pack(pady=10, padx=20, fill="x")
        
        self.lbl_msg = ctk.CTkLabel(self.frame_controls, text="Ready.", text_color="gray")
        self.lbl_msg.pack(pady=5)

        # --- START ENGINES ---
        # 1. Start the Background Ping Thread
        self.thread = threading.Thread(target=self.ping_loop, daemon=True)
        self.thread.start()

        # 2. Start the UI Update Loop
        self.update_ui_loop()

    # --- BACKGROUND THREAD (Runs in parallel) ---
    def ping_loop(self):
        while self.running:
            # Check ping
            ms = self.net_monitor.get_ping()
            self.current_ping = ms
            
            # Determine Color based on Lag
            if ms < 50:
                self.ping_status_color = "#00FF00" # Green
            elif ms < 100:
                self.ping_status_color = "#FFAA00" # Yellow
            else:
                self.ping_status_color = "#FF0000" # Red
            
            # Sleep 1.5s so we don't spam the network
            time.sleep(1.5)

    # --- MAIN UI LOOP (Runs on Main Thread) ---
    def update_ui_loop(self):
        # 1. Update CPU/RAM
        cpu = self.monitor.get_cpu_usage()
        ram = self.monitor.get_ram_usage()

        self.lbl_cpu.configure(text=f"CPU: {cpu}%")
        self.prog_cpu.set(cpu / 100)
        self.prog_cpu.configure(progress_color="red" if cpu > 85 else "#1f6aa5")

        self.lbl_ram.configure(text=f"RAM: {ram['percent']}% ({ram['used_gb']}GB Used)")
        self.prog_ram.set(ram['percent'] / 100)
        self.prog_ram.configure(progress_color="red" if ram['percent'] > 85 else "#1f6aa5")

        # 2. Update Ping (Read from the shared variable)
        self.lbl_ping.configure(text=f"Ping: {self.current_ping} ms", text_color=self.ping_status_color)
        
        if self.current_ping > 150:
            self.lbl_net_status.configure(text="LAG SPIKE DETECTED!", text_color="red")
        else:
            self.lbl_net_status.configure(text="Network Stable", text_color="gray")

        # Schedule next update in 500ms
        self.after(500, self.update_ui_loop)

    # --- BUTTON COMMANDS ---
    def toggle_mode(self):
        if self.switch_var.get() == "on":
            msg = self.power.set_high_performance()
            self.lbl_msg.configure(text=msg, text_color="#FF5555")
        else:
            msg = self.power.set_balanced()
            self.lbl_msg.configure(text=msg, text_color="white")

    def run_purge(self):
        self.lbl_msg.configure(text="Cleaning...", text_color="yellow")
        self.update()
        count, mb = self.optimizer.purge_bloatware()
        self.lbl_msg.configure(text=f"Killed {count} apps. Freed {mb} MB!", text_color="#00FF00")

    def on_closing(self):
        self.running = False
        self.destroy()

if __name__ == "__main__":
    app = DashboardApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()