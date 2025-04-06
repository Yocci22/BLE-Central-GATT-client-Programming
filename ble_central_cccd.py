import time
from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate, BTLEDisconnectError

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

# ✅ 添加 Notification 处理的 Delegate
class NotificationDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleNotification(self, cHandle, data):
        print("Notification received on handle", cHandle)
        print("Data (raw):", data)
        try:
            print("Data (decoded):", data.decode("utf-8"))
        except:
            print("Data could not be decoded as UTF-8.")

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

device_list = []

for n, dev in enumerate(devices):
    print("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi))
    device_list.append(dev)
    for (adtype, desc, value) in dev.getScanData():
        print(" %s = %s" % (desc, value))

number = input("Enter your device number: ")
num = int(number)
selected_dev = device_list[num]

print("Connecting to", selected_dev.addr, "with addrType", selected_dev.addrType)

try:
    dev = Peripheral(selected_dev.addr, selected_dev.addrType)
except BTLEDisconnectError as e:
    print("Connection failed:", e)
    exit(1)

# ✅ 设置 Notification Delegate
dev.setDelegate(NotificationDelegate())

print("Connected. Discovering services...")
for svc in dev.services:
    print(str(svc))

try:
    svc_uuid = UUID("0000fff0-0000-1000-8000-00805f9b34fb")
    char_uuid = UUID("0000fff2-0000-1000-8000-00805f9b34fb")

    testService = dev.getServiceByUUID(svc_uuid)
    chars = testService.getCharacteristics(char_uuid)
    if not chars:
        print("Characteristic not found.")
        dev.disconnect()
        exit(1)

    ec = chars[0]
    print("Characteristic handle:", ec.valHandle)

    dev.writeCharacteristic(ec.valHandle + 1, b"\x01\x00")
    print("CCCD set to 0x0001 (Notify enabled)")

    print("Waiting for notification...")
    while True:
        if dev.waitForNotifications(10.0):
            continue  # Notification handled by delegate
        print("No notification received in last 10 seconds.")
finally:
    print("Disconnecting.")
    dev.disconnect()
