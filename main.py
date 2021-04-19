from machine import Pin
import network
import time
import curl


def init_wifi(apname, password, timeout=3000):
    """Connect to wifi. A timeout (milliseconds) will cause the function to block
    until the timeout has expired or a successful connection is made."""
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(apname, password)
    if timeout > 0:
        time.sleep_ms(1000)
        now = time.ticks_ms()
        while True:
            if wifi.ifconfig()[0] != '0.0.0.0':
                print("Connected, IP: {}".format(wifi.ifconfig()[0]))
                break
            if time.ticks_ms() - now > timeout:
                break
    return wifi


wifi = init_wifi("wifi", "password")

p0 = Pin(25, Pin.OUT)
p1 = Pin(26, Pin.OUT)
p0.value(0)
p1.value(0)


def on_data(data):
    print(data)
    # rotate motor left
    if(data[2] == "left"):
        p0.value(1)
        p1.value(0)
    # rotate motor right
    elif(data[2] == "right"):
        p0.value(0)
        p1.value(1)

    # rotate it for 2 sec and then stop
    time.sleep(0.5)
    p0.value(0)
    p1.value(0)


local_name = 'diana'
unique_id = 'spool-motor4567'
mqtt = network.mqtt(local_name,
                    'mqtt://broker.hivemq.com',
                    clientid=unique_id,
                    data_cb=on_data
                    )

mqtt.start()
time.sleep(10)
connected = mqtt.subscribe('motor/cmd')
print("MQTT connected:", connected)
