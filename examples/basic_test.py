import tinytuya
DEVICE_ID = "YOUR_DEVICE_ID"
DEVICE_IP = "192.168.0.110"
LOCAL_KEY = "YOUR_LOCAL_KEY"
VERSION = 3.5

d = tinytuya.OutletDevice(DEVICE_ID, DEVICE_IP, LOCAL_KEY)
d.set_version(VERSION)
print("Status:")
print(d.status())
# print(d.set_value(1, True))          # Power on
# print(d.set_value(1, False))         # Power off
# print(d.set_value(101, "forceReset")) # Reset
