import subprocess
import re
import paho.mqtt.client as mqtt
import time

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    pass

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.on_log = on_log

mqttc.connect("192.168.12.1", 1883, 60)

mqttc.loop_start()



process = subprocess.Popen(
    [r'CapsuleClientExample.exe'],
    stdout=subprocess.PIPE,
    text=True
)

# Читаем построчно
for line in process.stdout:
    data = line.strip()
    #print(f"Получено из C++: {data}")

    match = re.search(r"([\d.eE+-]+);([\d.eE+-]+);([\d.eE+-]+)$", data)
    if match:
        a, b, t = map(float, match.groups())  # Преобразуем в float
        print(f"======> {a} {b} {t}")
        print(f'Дата: {data}')
        print('')
        if a > 0.55:
            infot = mqttc.publish("controller/action", "standDown", qos=2)
            infot.wait_for_publish()
            print("sit")
        else:
            infot = mqttc.publish("controller/action", "standUp", qos=2)
            infot.wait_for_publish()
            #print("")
    else:
        print(f"<<<<<<<<<<<<")
