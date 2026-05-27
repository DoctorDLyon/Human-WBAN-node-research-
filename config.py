"""Centralized configuration for WBAN Node Research application."""
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class BLEConfig:
    """Bluetooth Low Energy configuration."""
    scan_duration: float = 5.0
    scan_interval: float = 0.1
    connect_timeout: float = 10.0
    disconnect_timeout: float = 5.0
    rssi_threshold: int = -100
    manufacturer_data_filter: bool = True
    service_uuid_filter: bool = True


@dataclass
class DatabaseConfig:
    """Database configuration."""
    db_path: str = str(Path.home() / ".wban" / "sensors.db")
    auto_backup: bool = True
    backup_interval: int = 3600  # seconds
    max_readings_buffer: int = 10000
    enable_wal: bool = True  # Write-Ahead Logging


@dataclass
class UIConfig:
    """User interface configuration."""
    theme: str = "dark"  # dark or light
    window_width: int = 1400
    window_height: int = 900
    update_interval: int = 500  # ms
    graph_history_points: int = 500
    enable_animations: bool = True


@dataclass
class LoggingConfig:
    """Logging configuration."""
    log_dir: str = str(Path.home() / ".wban" / "logs")
    log_level: str = "INFO"
    max_log_size: int = 10485760  # 10MB
    backup_count: int = 5
    enable_file_logging: bool = True
    enable_console_logging: bool = True


@dataclass
class SensorProfiles:
    """Known sensor profiles and their characteristics."""
    
    PROFILES: Dict[str, Dict] = None
    
    def __post_init__(self):
        if self.PROFILES is None:
            self.PROFILES = {
                "ECG": {
                    "name": "Electrocardiogram",
                    "sampling_rate": 250,
                    "channels": 1,
                    "unit": "mV",
                    "protocol": "BLE_GATT",
                },
                "EMG": {
                    "name": "Electromyography",
                    "sampling_rate": 1000,
                    "channels": 8,
                    "unit": "µV",
                    "protocol": "BLE_GATT",
                },
                "EEG": {
                    "name": "Electroencephalography",
                    "sampling_rate": 256,
                    "channels": 8,
                    "unit": "µV",
                    "protocol": "BLE_GATT",
                },
                "TEMP": {
                    "name": "Temperature",
                    "sampling_rate": 1,
                    "channels": 1,
                    "unit": "°C",
                    "protocol": "BLE_GATT",
                },
                "SPO2": {
                    "name": "Oxygen Saturation",
                    "sampling_rate": 1,
                    "channels": 1,
                    "unit": "%",
                    "protocol": "BLE_GATT",
                },
                "HR": {
                    "name": "Heart Rate",
                    "sampling_rate": 1,
                    "channels": 1,
                    "unit": "bpm",
                    "protocol": "BLE_GATT",
                },
                "GLUCOSE": {
                    "name": "Glucose Monitoring",
                    "sampling_rate": 1,
                    "channels": 1,
                    "unit": "mg/dL",
                    "protocol": "BLE_GATT",
                },
                "ACCEL": {
                    "name": "Accelerometer",
                    "sampling_rate": 100,
                    "channels": 3,
                    "unit": "g",
                    "protocol": "BLE_GATT",
                },
                "GYRO": {
                    "name": "Gyroscope",
                    "sampling_rate": 100,
                    "channels": 3,
                    "unit": "°/s",
                    "protocol": "BLE_GATT",
                },
                "PRESSURE": {
                    "name": "Barometric Pressure",
                    "sampling_rate": 1,
                    "channels": 1,
                    "unit": "hPa",
                    "protocol": "BLE_GATT",
                },
            }


@dataclass
class SafetyConfig:
    """Safety and control settings."""
    require_confirmation_for_termination: bool = True
    auto_backup_before_termination: bool = True
    max_connection_attempts: int = 3
    command_timeout: float = 30.0
    enable_force_termination: bool = True
    log_all_operations: bool = True


class AppConfig:
    """Master configuration class."""
    
    def __init__(self):
        self.ble = BLEConfig()
        self.database = DatabaseConfig()
        self.ui = UIConfig()
        self.logging = LoggingConfig()
        self.sensor_profiles = SensorProfiles()
        self.safety = SafetyConfig()
        
        # Create directories if they don't exist
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories."""
        Path(self.database.db_path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.logging.log_dir).mkdir(parents=True, exist_ok=True)
    
    def get_sensor_profile(self, sensor_type: str) -> Dict:
        """Get sensor profile by type."""
        return self.sensor_profiles.PROFILES.get(
            sensor_type.upper(),
            {
                "name": "Unknown",
                "sampling_rate": 0,
                "channels": 0,
                "unit": "Unknown",
                "protocol": "Unknown",
            }
        )
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary."""
        return {
            "ble": self.ble.__dict__,
            "database": self.database.__dict__,
            "ui": self.ui.__dict__,
            "logging": self.logging.__dict__,
            "safety": self.safety.__dict__,
        }


# Global config instance
config = AppConfig()
