import time
from pyduino import Arduino

a = Arduino()
time.sleep(3)
a.set_pin_mode(12,'O')
a.set_pin_mode(12,'I')
time.sleep(1)
a.digital_write(12,0)
a.analog_write(5,245)
print(a.digital_read(12))
print(a.analog_read(2))
time.sleep(5)