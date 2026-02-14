# 🛠️ Latency Assassin: Official Changelog

All notable changes to the **Latency Assassin** project are documented here, tracking the evolution from a basic system hook to a high-end interactive glass console.

---

## [v9.0] - 2026-02-14
### Added
- **Triple-Bar HUD:** Integrated simultaneous live tracking for CPU, iGPU, and System RAM.
- **Interactive Window Controls:** Custom close (✕) and minimize (—) buttons built into the sidebar to replace the standard OS title bar.
- **Click-to-Drag:** Implemented manual window repositioning logic for the borderless interface.
- **iGPU Logic:** Added specialized monitoring for Integrated Graphics load on Intel/Windows systems.

## [v8.0] - 2026-02-14
### Added
- **Cinematic Fade Engine:** Implemented a 1.2-second alpha transition (0.2 to 0.95) for a "heavy" premium feel.
- **Caviar Aesthetic:** Transitioned typography to **Century Gothic** for a geometric, minimalist look.
- **Jitter Tracking:** Added variance calculation between consecutive pings to monitor network stability beyond raw latency.

## [v7.0] - 2026-02-14
### Added
- **Curvy Geometry:** Implemented `overrideredirect` and high `corner_radius` for an organic, rounded glass shape.
- **Dynamic Hover Layer:** Linked the Windows Alpha API to mouse hover events (`<Enter>`/`<Leave>`).

## [v4.0 - v6.0] - 2026-02-14
### Added
- **Glassmorphism Design:** Semi-transparent backgrounds with high-contrast borders.
- **Sidebar Architecture:** Moved to a modular layout to separate system uptime/branding from active controls.
- **Dynamic Glow:** Color-coded status updates (Cyan for healthy, Orange/Red for system stress).



## [v3.0.0] - 2026-02-14
### Added
- **Threading Engine:** Implemented background threading to handle Network I/O, ensuring the GUI remains responsive during ping requests.
- **Network Radar:** Integrated ICMP tracking to Google DNS (8.8.8.8).



## [v2.0.0] - 2026-02-14
### Added
- **Power Controller:** Added `subprocess` logic to automate switching between Windows Balanced and High-Performance power schemes.
- **RAM Purge:** Developed "Hit List" logic to identify and terminate memory-heavy background processes (Chrome, Discord, etc.).

## [1.0.0] - 2026-02-14
### Added
- **Core Foundation:** Initial build using `psutil` and `CustomTkinter`.
- **System Hooks:** Basic real-time CPU and RAM percentage monitoring.

---
*Built for the Asus Vivobook (12th Gen Intel Architecture)*