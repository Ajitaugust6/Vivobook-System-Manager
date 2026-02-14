# Changelog

All notable changes to the **Latency Assassin** project will be documented in this file.

## [3.0.0] - 2026-02-14
### Added
- **Threading Engine:** Implemented `threading` to handle network I/O without blocking the GUI.
- **Network Radar:** Added ICMP ping tracking to `8.8.8.8` with visual jitter status.
- **Improved UI:** Updated to a 500x600 layout with dedicated network and stat frames.

## [2.0.0] - 2026-02-12
### Added
- **Power Controller:** Added `subprocess` logic to toggle Windows High Performance power plans.
- **RAM Purge:** Created a "Hit List" logic to terminate background bloatware via PIDs.

## [1.0.0] - 2026-02-10
### Added
- Initial release with basic CPU and RAM monitoring using `psutil` and `CustomTkinter`.