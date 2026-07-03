# Changelog

All notable changes to the Hanchu ESS BLE integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.0.7] - 2026-07-03

### Fixed

- Load Power sensor now correctly nets off PV generation on non-AC-coupled
  (DC-coupled/hybrid) systems. Previously the calculation only read AC
  Coupled PV Power (P237), which stays at 0 on non-AC-coupled hardware,
  causing Load Power to be overstated by the full PV generation amount
  during daylight hours on those systems. Now sums P060 (PV Total Power)
  and P237, which are mutually exclusive by hardware type — one is always
  0 depending on coupling configuration — so the fix works correctly on
  both AC-coupled and non-AC-coupled systems without needing to know
  which type is connected. Thanks to a community contributor for
  identifying the gap and confirming the register behaviour on their
  non-AC-coupled setup.

## [1.0.6] - 2026-07-02

### Fixed
- Time slot entities (`time.py`) no longer get stuck showing a requested
  value indefinitely after a failed write. Previously, if a BLE write
  timed out or the device didn't confirm success, `_pending_value` was
  never cleared, so the entity kept displaying the target time even though
  the device never actually accepted it. On failure, the entity now
  reverts to whatever the coordinator last actually read from the device.

## [1.0.5] - 2026-06-26

### Added
- Diagnostic sensors: Last BLE Read, Consecutive Failures, Cycle Duration
- Contributions from PaulDGAL

## [1.0.4] - 2026-06-26

### Changed
- Replaced flat 30-second polling with a two-tier fast/slow poll system

## [1.0.3] - 2026-06-26

### Fixed
- Load Power sign convention corrected using `abs(P237)`

## [1.0.2] - 2026-06-26

### Changed
- General reliability and polling improvements following initial release

## [1.0.1] - 2026-06-19

### Fixed
- Minor fixes following initial release

## [1.0.0] - 2026-06-19

### Added
- Initial release: local Bluetooth control for Hanchu iESS battery systems
- P/L-code protocol mapping including Grid Power, Battery Power, Battery
  Capacity, AC Coupled PV Power, and charge/discharge SOC limits
- `asyncio.Lock` to serialise BLE reads/writes
- CoordinatorEntity-based entities for charge/discharge time slots and
  sensors


[Unreleased]: https://github.com/upton68/hanchu-ess-ble/compare/v1.0.7...HEAD
[1.0.7]: https://github.com/upton68/hanchu-ess-ble/compare/v1.0.6...v1.0.7  
[1.0.6]: https://github.com/upton68/hanchu-ess-ble/compare/v1.0.5...v1.0.6
[1.0.5]: https://github.com/upton68/hanchu-ess-ble/compare/v1.0.4...v1.0.5
[1.0.4]: https://github.com/upton68/hanchu-ess-ble/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/upton68/hanchu-ess-ble/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/upton68/hanchu-ess-ble/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/upton68/hanchu-ess-ble/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/upton68/hanchu-ess-ble/compare/v1.0.0
