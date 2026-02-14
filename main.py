import customtkinter as ctk
import threading
import time
import sys
from monitor import SystemMonitor, PowerController, MemoryOptimizer, NetworkRadar

class LatencyAssassin(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- DYNAMIC WINDOW CONFIG ---
        self.target_alpha = 0.2
        self.current_alpha = 0.2
        self.geometry("640x480")
        self.attributes("-alpha", self.current_alpha)
        self.attributes("-topmost", True)
        self.overrideredirect(True) # Curvy rounded edge mode

        # Logic
        self.monitor = SystemMonitor(); self.power = PowerController()
        self.opt = MemoryOptimizer(); self.radar = NetworkRadar()
        self.ping = 0; self.jitter = 0; self.running = True

        # Drag Functionality
        self.bind("<Button-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)

        # --- UI: MAIN ROUNDED FRAME ---
        self.glass_panel = ctk.CTkFrame(self, corner_radius=35, fg_color="#080B12", border_width=2, border_color="#1F2937")
        self.glass_panel.pack(fill="both", expand=True, padx=5, pady=5)

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self.glass_panel, width=180, corner_radius=35, fg_color="#0D1117")
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        self.sidebar.pack_propagate(False)

        # Window Controls
        self.ctrl = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.ctrl.pack(fill="x", pady=15, padx=10)
        ctk.CTkButton(self.ctrl, text="✕", width=28, height=28, fg_color="#DA3633", hover_color="#B62324", corner_radius=14, command=self.exit_app).pack(side="right", padx=2)
        ctk.CTkButton(self.ctrl, text="—", width=28, height=28, fg_color="#30363D", hover_color="#484F58", corner_radius=14, command=self.minimize_app).pack(side="right", padx=2)

        self.logo = ctk.CTkLabel(self.sidebar, text="LATENCY\nASSASSIN", font=("Century Gothic", 20, "bold"), text_color="#00F2FF")
        self.logo.pack(pady=20)
        
        self.uptime_lbl = ctk.CTkLabel(self.sidebar, text="UPTIME: 00:00", font=("Century Gothic", 12), text_color="gray")
        self.uptime_lbl.pack(side="bottom", pady=30)

        # MAIN CONSOLE
        self.main = ctk.CTkFrame(self.glass_panel, fg_color="transparent")
        self.main.pack(side="right", fill="both", expand=True, padx=25, pady=25)

        # 1. NETWORK RADAR (Latency + Jitter)
        self.net_hud = ctk.CTkFrame(self.main, fg_color="transparent")
        self.net_hud.pack(fill="x", pady=(0, 10))
        self.ping_lbl = ctk.CTkLabel(self.net_hud, text="-- MS", font=("Century Gothic", 45, "bold"), text_color="#00F2FF")
        self.ping_lbl.pack(side="left", expand=True)
        self.jitter_lbl = ctk.CTkLabel(self.net_hud, text="JITTER: --", font=("Century Gothic", 12), text_color="#D29922")
        self.jitter_lbl.pack(side="right", padx=10)

        # 2. LIVE RESOURCE HUDS
        self.cpu_bar = self.create_hud("CPU LOAD", "#00F2FF")
        self.gpu_bar = self.create_hud("iGPU LOAD", "#A855F7")
        self.ram_bar = self.create_hud("MEMORY", "#3FB950")

        # 3. COMMANDS
        self.p_var = ctk.StringVar(value="off")
        ctk.CTkSwitch(self.main, text="PERFORMANCE PROTOCOL", font=("Century Gothic", 12), variable=self.p_var, command=self.toggle_power, progress_color="#00F2FF").pack(pady=10)
        ctk.CTkButton(self.main, text="EXECUTE RAM PURGE", font=("Century Gothic", 14, "bold"), fg_color="#EF4444", height=45, corner_radius=22, command=self.run_purge).pack(fill="x", pady=10)

        self.status = ctk.CTkLabel(self.main, text="SYSTEM NOMINAL", font=("Century Gothic", 10), text_color="gray")
        self.status.pack(side="bottom")

        # --- BINDINGS & THREADS ---
        self.bind("<Enter>", lambda e: self.set_fade(0.95))
        self.bind("<Leave>", lambda e: self.set_fade(0.2))
        
        threading.Thread(target=self.radar_thread, daemon=True).start()
        self.update_ui(); self.fade_engine()

    def create_hud(self, name, color):
        ctk.CTkLabel(self.main, text=name, font=("Century Gothic", 10), text_color="gray").pack(anchor="w", padx=10)
        bar = ctk.CTkProgressBar(self.main, height=10, corner_radius=10, progress_color=color, fg_color="#1F2937")
        bar.pack(fill="x", padx=10, pady=(2, 10))
        bar.set(0)
        return bar

    # Fade Logic
    def set_fade(self, val): self.target_alpha = val
    def fade_engine(self):
        step = 0.04
        if abs(self.current_alpha - self.target_alpha) > 0.01:
            self.current_alpha += step if self.current_alpha < self.target_alpha else -step
            self.attributes("-alpha", self.current_alpha)
        self.after(50, self.fade_engine)

    # Window Actions
    def start_move(self, event): self.x = event.x; self.y = event.y
    def do_move(self, event):
        x, y = self.winfo_x() + (event.x - self.x), self.winfo_y() + (event.y - self.y)
        self.geometry(f"+{x}+{y}")

    def minimize_app(self): self.attributes("-alpha", 0); self.state('iconic')
    def exit_app(self): self.running = False; self.destroy(); sys.exit()

    def radar_thread(self):
        while self.running:
            self.ping, self.jitter = self.radar.get_stats(); time.sleep(1.5)

    def update_ui(self):
        cpu, gpu, ram = self.monitor.get_cpu_usage(), self.monitor.get_gpu_usage(), self.monitor.get_ram_usage()
        self.cpu_bar.set(cpu / 100); self.gpu_bar.set(gpu / 100); self.ram_bar.set(ram['percent'] / 100)
        self.ping_lbl.configure(text=f"{self.ping} MS"); self.jitter_lbl.configure(text=f"JITTER: {self.jitter}ms")
        self.uptime_lbl.configure(text=f"UPTIME: {self.monitor.get_uptime()}")
        self.after(1000, self.update_ui)

    def toggle_power(self):
        self.status.configure(text=self.power.set_high_performance() if self.p_var.get() == "on" else self.power.set_balanced())

    def run_purge(self):
        k, m = self.opt.purge()
        self.status.configure(text=f"PURGED {k} APPS | {m}MB FREED", text_color="#10B981")

if __name__ == "__main__":
    app = LatencyAssassin(); app.mainloop()