import asyncio
import threading
import time
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

class BLEScanner:
    def __init__(self, discovery_callback, scan_stopped_callback=None):
        self.scanner = None
        self.is_scanning = False
        self.discovery_callback = discovery_callback
        self.scan_stopped_callback = scan_stopped_callback
        self.found_devices = {}  # Store devices to avoid duplicates and update RSSI

    def calculate_distance(self, rssi, tx_power=-59):
        """
        Estimates distance based on RSSI.
        Formula: 10^((tx_power - rssi) / (10 * n))
        n = 2 (free space), usually 2-4 for indoor.
        """
        if rssi == 0:
            return -1.0
        ratio = rssi * 1.0 / tx_power
        if ratio < 1.0:
            return pow(ratio, 10)
        else:
            distance = (0.89976) * pow(ratio, 7.7095) + 0.111
            return distance

    def calculate_signal_percent(self, rssi):
        """Converts RSSI (typically -100 to -20) to a 0-100% scale."""
        # Clamp values
        if rssi <= -100: return 0
        if rssi >= -20: return 100
        # Linear interpolation
        return int(((rssi + 100) / 80) * 100)

    async def _run_scan(self):
        self.is_scanning = True
        self.found_devices = {}

        def detection_handler(device: BLEDevice, adv: AdvertisementData):
            if not self.is_scanning:
                return

            address = device.address
            # Prefer advertisement RSSI if available, otherwise device.rssi
            rssi = getattr(adv, "rssi", None) or getattr(device, "rssi", None)
            if rssi is None:
                # Skip if no RSSI available
                return
            
            # Calculate metrics
            distance = self.calculate_distance(rssi)
            signal_pct = self.calculate_signal_percent(rssi)
            
            # Update or add device
            # We store the object to fetch services later if needed
            device_data = {
                "name": device.name or "Unknown",
                "address": address,
                "rssi": rssi,
                "signal_pct": signal_pct,
                "distance": distance,
                "last_seen": time.strftime("%H:%M:%S"),
                "connectable": getattr(adv, "is_connectable", False),
                "services_count": len(getattr(adv, "service_uuids", []) ) # Count UUIDs found in advertisement
            }

            self.found_devices[address] = device_data
            
            # Send data to GUI
            if self.discovery_callback:
                try:
                    self.discovery_callback(device_data)
                except Exception:
                    # Guard against callback exceptions from different threads
                    pass

        try:
            # detection_callback is called directly by bleak
            self.scanner = BleakScanner(detection_callback=detection_handler)
            await self.scanner.start()
            
            # Keep scanning until stopped
            while self.is_scanning:
                await asyncio.sleep(0.5)
                
        except Exception as e:
            print(f"Scan error: {e}")
        finally:
            if self.scanner:
                await self.scanner.stop()
            self.is_scanning = False
            if self.scan_stopped_callback:
                try:
                    self.scan_stopped_callback(len(self.found_devices))
                except Exception:
                    pass

    def start_scan(self):
        if self.is_scanning:
            return
        # Run in a daemon thread so it doesn't block app exit
        thread = threading.Thread(target=lambda: asyncio.run(self._run_scan()), daemon=True)
        thread.start()

    def stop_scan(self):
        self.is_scanning = False
