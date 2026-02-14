# ⚡ LATENCY ASSASSIN // VIVOBOOK COMMANDER
> **High-performance system monitoring & optimization suite for 12th Gen Intel Architecture.**

Latency Assassin is a custom-built, glassmorphism-inspired dashboard designed to monitor and optimize the Asus Vivobook. It bridges the gap between raw hardware data and actionable gaming performance.



## 🚀 Key Features
* **Network Radar:** Real-time ICMP ping tracking to `8.8.8.8` with **Jitter** variance analysis.
* **Triple-HUD Monitoring:** Live tracking of **CPU Load**, **iGPU Utilization**, and **Physical RAM** consumption.
* **Performance Protocols:** Subprocess-based toggling between Windows *Balanced* and *High Performance* power plans.
* **Cinematic UX:** 1.2s smooth-fade transparency engine (0.2 to 0.95 alpha) and borderless rounded geometry.
* **Memory Purge:** One-click termination of non-essential background bloatware via PID "Hit List" logic.

## 🛠️ Technical Stack
* **Language:** Python 3.10+
* **GUI:** CustomTkinter (Modern UI Framework)
* **Logic:** `psutil` (System Hooks), `subprocess` (Power GUID management)
* **Concurrency:** Multi-threading for non-blocking Network I/O.
* **OS:** Windows 10/11 (Optimized for Asus hardware)

## 📸 Interface Preview
The interface features a **Caviar-inspired** geometric aesthetic.
* **Dashboard State:** 20% Transparency (Idle) / 95% Transparency (Active).
* **Resolution:** Fixed 640x480 "Dashboard" footprint.



## 🔧 Installation & Usage
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Ajitaugust6/Vivobook-System-Manager.git](https://github.com/Ajitaugust6/Vivobook-System-Manager.git)
   ```
2. **Install Dependencies:**
   ```bash
   pip install customtkinter psutil
   ```
3. **Run the Dashboard:**
   ```bash
   python main.py
   ```

## 📋 License
MIT License