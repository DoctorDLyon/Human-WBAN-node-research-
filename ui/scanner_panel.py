"""
Scanner Panel - Real-time BLE device discovery interface (integrated with BLEScanner)
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel, QSpinBox,
                             QCheckBox, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QIcon
import logging

# Import BLEScanner that you added to bleak/backends/device.py
from bleak.backends.device import BLEScanner

logger = logging.getLogger(__name__)


class ScannerPanel(QWidget):
    """Panel for discovering and scanning BLE devices"""

    device_selected = pyqtSignal(str)  # device_address
    device_double_clicked = pyqtSignal(str)

    # Internal signals to marshal background thread callbacks to the GUI thread
    device_discovered = pyqtSignal(dict)    # payload: device_data dict
    scan_stopped = pyqtSignal(int)          # payload: total found count

    def __init__(self):
        super().__init__()
        self.devices = {}         # maps address -> device_data dict
        self.is_scanning = False
        self.ble_scanner = None
        self.init_ui()

        # Connect internal signals to slots
        self.device_discovered.connect(self._on_device_found_from_signal)
        self.scan_stopped.connect(self._on_scan_stopped_from_signal)

        # Initialize BLEScanner
        # discovery_callback will emit device_discovered signal (thread-safe)
        self.ble_scanner = BLEScanner(
            discovery_callback=lambda d: self.device_discovered.emit(d),
            scan_stopped_callback=lambda n: self.scan_stopped.emit(n)
        )

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
        if self.is_scanning:
            return
        self.is_scanning = True
        self.scan_button.setText("Stop Scan")
        self.scan_button.setStyleSheet("background-color: #ff6b6b;")
        self.status_label.setText("Scanning for BLE devices...")
        logger.info("Scanner started")

        # Clear previous results if desired; keep them by default
        # self.clear_results()

        # Start the BLEScanner
        try:
            self.ble_scanner.start_scan()
        except Exception as e:
            logger.exception("Failed to start BLE scanner: %s", e)
            QMessageBox.warning(self, "Scan Error", f"Could not start scan: {e}")
            self.is_scanning = False
            self.scan_button.setText("Start Scan")
            self.scan_button.setStyleSheet("")

    def stop_scan(self):
        """Stop BLE scanning"""
        if not self.is_scanning:
            return
        self.ble_scanner.stop_scan()
        # Actual UI text update will happen when scan_stopped signal arrives
        self.status_label.setText("Stopping scan...")

    def _on_device_found_from_signal(self, device_data: dict):
        """Slot running on GUI thread called when device_discovered signal emits"""
        if not self.auto_update.isChecked():
            # still store latest data but don't update the table
            self.devices[device_data["address"]] = device_data
            self.device_count_label.setText(f"Found: {len(self.devices)} devices")
            return

        # Apply RSSI threshold
        threshold = self.rssi_spinbox.value()
        if device_data.get("rssi", -999) < threshold:
            # if already tracked, remove from table? We'll keep tracked devices but not show them.
            # simply update stored dict and refresh visible table
            self.devices[device_data["address"]] = device_data
            self._refresh_table()
            return

        # Insert or update row for this device
        address = device_data["address"]
        row_index = self.find_row_by_address(address)

        if row_index == -1:
            row_index = self.device_table.rowCount()
            self.device_table.insertRow(row_index)
            # Make address item non-editable
            address_item = QTableWidgetItem(address)
            address_item.setFlags(address_item.flags() & ~Qt.ItemIsEditable)
            self.device_table.setItem(row_index, 1, address_item)

        # Update stored entry
        self.devices[address] = device_data

        # 0: Name
        self.device_table.setItem(row_index, 0, QTableWidgetItem(device_data.get("name", "Unknown")))
        # 2: RSSI
        self.device_table.setItem(row_index, 2, QTableWidgetItem(str(device_data.get("rssi", ""))))
        # 3: Signal %
        self.device_table.setItem(row_index, 3, QTableWidgetItem(f"{device_data.get('signal_pct', 0)}%"))
        # 4: Distance
        dist = device_data.get("distance", -1)
        dist_val = f"{dist:.2f}" if isinstance(dist, (int, float)) and dist > 0 else "N/A"
        self.device_table.setItem(row_index, 4, QTableWidgetItem(dist_val))
        # 5: Connectable
        conn_val = "Yes" if device_data.get("connectable", False) else "No"
        self.device_table.setItem(row_index, 5, QTableWidgetItem(conn_val))
        # 6: Last Seen
        last_seen = device_data.get("last_seen", "")
        self.device_table.setItem(row_index, 6, QTableWidgetItem(last_seen))
        # 7: Services (Count)
        self.device_table.setItem(row_index, 7, QTableWidgetItem(str(device_data.get("services_count", 0))))

        # Update counts and status
        self.device_count_label.setText(f"Found: {len(self.devices)} devices")
        self.status_label.setText(f"Showing {self.device_table.rowCount()} devices (threshold: {threshold} dBm)")

    def _refresh_table(self):
        """Rebuild visible table rows based on current self.devices and RSSI threshold"""
        threshold = self.rssi_spinbox.value()
        self.device_table.setRowCount(0)
        for addr, device_data in self.devices.items():
            if device_data.get("rssi", -999) < threshold:
                continue
            row = self.device_table.rowCount()
            self.device_table.insertRow(row)
            self.device_table.setItem(row, 0, QTableWidgetItem(device_data.get("name", "Unknown")))
            addr_item = QTableWidgetItem(addr)
            addr_item.setFlags(addr_item.flags() & ~Qt.ItemIsEditable)
            self.device_table.setItem(row, 1, addr_item)
            self.device_table.setItem(row, 2, QTableWidgetItem(str(device_data.get("rssi", ""))))
            self.device_table.setItem(row, 3, QTableWidgetItem(f"{device_data.get('signal_pct', 0)}%"))
            dist = device_data.get("distance", -1)
            dist_val = f"{dist:.2f}" if isinstance(dist, (int, float)) and dist > 0 else "N/A"
            self.device_table.setItem(row, 4, QTableWidgetItem(dist_val))
            self.device_table.setItem(row, 5, QTableWidgetItem("Yes" if device_data.get("connectable", False) else "No"))
            self.device_table.setItem(row, 6, QTableWidgetItem(device_data.get("last_seen", "")))
            self.device_table.setItem(row, 7, QTableWidgetItem(str(device_data.get("services_count", 0))))
        self.device_count_label.setText(f"Found: {len(self.devices)} devices")
        self.status_label.setText(f"Showing {self.device_table.rowCount()} devices (threshold: {threshold} dBm)")

    def find_row_by_address(self, address):
        """Helper to find existing row by address to update it instead of duplicating."""
        for row in range(self.device_table.rowCount()):
            item = self.device_table.item(row, 1)  # Check Address column
            if item and item.text() == address:
                return row
        return -1

    def _on_scan_stopped_from_signal(self, total_found: int):
        """Slot when the scan actually stops (arrives from BLEScanner)"""
        self.is_scanning = False
        self.scan_button.setText("Start Scan")
        self.scan_button.setStyleSheet("")
        self.status_label.setText(f"Scan stopped. Found {total_found} devices.")
        logger.info("Scanner stopped with %d devices", total_found)

        # Optionally refresh table after scan ends (respects threshold)
        self._refresh_table()

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
