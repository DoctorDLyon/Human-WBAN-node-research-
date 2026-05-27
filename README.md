# Human WBAN Node Research

## Overview
A comprehensive application for discovering, identifying, and managing Body Area Network (BAN) sensors and wearables using Bluetooth Low Energy (BLE) technology. This tool enables researchers to:

- **Discover** hidden and visible BLE sensors within human biological body networks
- **Identify** sensor types, capabilities, and network topology
- **Monitor** real-time sensor data and metrics
- **Control** sensor functions and parameters
- **Terminate** sensor operations when necessary

## Features

### Core Capabilities
- **BLE Scanner**: Real-time discovery of nearby BLE devices with signal strength monitoring
- **Sensor Database**: Comprehensive registry of known sensor types and profiles
- **Device Control**: Modify sensor parameters, firmware, and operational modes
- **Data Monitor**: Stream and visualize sensor data in real-time
- **Command Interface**: Execute predefined and custom commands on devices
- **Device Termination**: Safely disable or power down sensors
- **Session Logging**: Complete audit trail of all operations

## Technology Stack
- **Python 3.8+**
- **Bleak**: BLE communication
- **PyQt6**: User interface
- **SQLite**: Sensor database
- **Asyncio**: Asynchronous operations

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Project Structure

```
Human-WBAN-node-research/
├── README.md
├── requirements.txt
├── main.py
├── config.py
├── src/
│   ├── ble_manager.py          # Core BLE scanning and connection
│   ├── sensor_models.py        # Sensor data structures
│   ├── sensor_database.py      # Sensor registry and lookup
│   ├── device_controller.py    # Device command execution
│   ├── data_monitor.py         # Real-time data streaming
│   └── utils.py                # Utility functions
├── ui/
│   ├── main_window.py          # Primary UI window
│   ├── scanner_panel.py        # Device discovery interface
│   ├── device_details.py       # Device information display
│   ├── control_panel.py        # Command execution interface
│   ├── data_viewer.py          # Real-time data visualization
│   └── styles.py               # UI styling
└── tests/
    ├── test_ble_manager.py
    ├── test_sensor_models.py
    ├── test_device_controller.py
    └── test_data_monitor.py
```

## License
Apache License 2.0
