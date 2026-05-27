"""
Scanner Panel - Real-time BLE device discovery interface
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel, QSpinBox,
                             QCheckBox, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QColor, QIcon
import logging

logger = logging.getLogger(__name__)


class ScannerPanel(QWidget):
    """Panel for discovering and scanning BLE devices"""

    device_selected = pyqtSignal(str)  # device_address
    device_double_clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.devices = {}
        self.is_scanning = False
        self.init_ui()

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()

        # Control panel
        control_layout = QHBoxLayout()
        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.toggle_scan)
        control_layout.addWidget(self.scan_button)

        self.clear_button = QPushButton("Clear Results")
        self.clear_button.clicked.connect(self.clear_results)
        control_layout.addWidget(self.clear_button)

        control_layout.addStretch()

        # Filter options
        self.filter_label = QLabel("RSSI Threshold:")
        self.rssi_spinbox = QSpinBox()
        self.rssi_spinbox.setRange(-100, 0)
        self.rssi_spinbox.setValue(-80)
        self.rssi_spinbox.setSuffix(" dBm")
        control_layout.addWidget(self.filter_label)
        control_layout.addWidget(self.rssi_spinbox)

        self.auto_update = QCheckBox("Auto Update")
        self.auto_update.setChecked(True)
        control_layout.addWidget(self.auto_update)

        layout.addLayout(control_layout)

        # Device table
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(8)
        self.device_table.setHorizontalHeaderLabels([
            "Device Name", "Address", "RSSI (dBm)", "Signal %", "Distance (m)",
            "Connectable", "Last Seen", "Services"
        ])
        self.device_table.itemSelectionChanged.connect(self.on_device_selected)
        self.device_table.itemDoubleClicked.connect(self.on_device_double_clicked)

        # Configure columns
        header = self.device_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.device_table)

        # Status bar
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Ready. Click 'Start Scan' to begin.")
        self.device_count_label = QLabel("Found: 0 devices")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.device_count_label)
        layout.addLayout(status_layout)

        self.setLayout(layout)

    def toggle_scan(self):
        """Toggle scanning on/off"""
        if not self.is_scanning:
            self.start_scan()
        else:
            self.stop_scan()

    def start_scan(self):
        """Start BLE scanning"""
        self.is_scanning = True
        self.scan_button.setText("Stop Scan")
        self.scan_button.setStyleSheet("background-color: #ff6b6b;")
        self.status_label.setText("Scanning for BLE devices...")
        logger.info("Scanner started")

    def stop_scan(self):
        """Stop BLE scanning"""
        self.is_scanning = False
        self.scan_button.setText("Start Scan")
        self.scan_button.setStyleSheet("")
        self.status_label.setText("Scan stopped. Found {} devices.".format(len(self.devices)))
        logger.info("Scanner stopped")

    def update_devices(self, devices: list):
        """Update device table with discovered devices"""
        if not self.auto_update.isChecked():
            return

        threshold = self.rssi_spinbox.value()
        self.device_table.setRowCount(0)

        for device in devices:
            if device.rssi < threshold:
                continue

            self.devices[device.address] = device

            row = self.device_table.rowCount()
            self.device_table.insertRow(row)

            # Device name
            name_item = QTableWidgetItem(device.name)
            self.device_table.setItem(row, 0, name_item)

            # Address
            addr_item = QTableWidgetItem(device.address)
            self.device_table.setItem(row, 1, addr_item)

            # RSSI
            rssi_item = QTableWidgetItem(str(device.rssi))
            self.device_table.setItem(row, 2, rssi_item)

            # Signal strength
            signal_item = QTableWidgetItem(f"{device.signal_strength:.0f}%")
            self.device_table.setItem(row, 3, signal_item)

            # Distance
            distance_item = QTableWidgetItem(f"{device.distance:.2f}")
            self.device_table.setItem(row, 4, distance_item)

            # Connectable
            conn_item = QTableWidgetItem("Yes" if device.is_connectable else "No")
            self.device_table.setItem(row, 5, conn_item)

            # Last seen
            last_seen = device.last_seen.strftime("%H:%M:%S")
            seen_item = QTableWidgetItem(last_seen)
            self.device_table.setItem(row, 6, seen_item)

            # Services count
            services_item = QTableWidgetItem(str(len(device.services)))
            self.device_table.setItem(row, 7, services_item)

        self.device_count_label.setText(f"Found: {len(self.devices)} devices")
        self.status_label.setText(f"Showing {self.device_table.rowCount()} devices (threshold: {threshold} dBm)")

    def on_device_selected(self):
        """Handle device selection"""
        selected_rows = self.device_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            address = self.device_table.item(row, 1).text()
            self.device_selected.emit(address)

    def on_device_double_clicked(self, item):
        """Handle device double click"""
        address = self.device_table.item(item.row(), 1).text()
        self.device_double_clicked.emit(address)

    def clear_results(self):
        """Clear scan results"""
        self.device_table.setRowCount(0)
        self.devices.clear()
        self.device_count_label.setText("Found: 0 devices")
        self.status_label.setText("Results cleared.")

    def get_selected_device(self) -> str:
        """Get currently selected device address"""
        selected_rows = self.device_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            return self.device_table.item(row, 1).text()
        return ""
