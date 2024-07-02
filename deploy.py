from robot import Robot, Node, Edge
import paho.mqtt.client as mqtt
import json
from datetime import datetime


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("kobuki/v2/ic/0001/order")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Set last will
message = {
    "headerId": 0,
    "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ"),
    "version": "2.0.0",
    "manufacturer": "IC",
    "serialNumber": "0001",
    "connectionState": "CONNECTIONBROKEN"
}

mqttc.will_set("kobuki/v2/ic/0001/connection", json.dumps(message), qos=1, retain=True)

# Estabilish connection
mqttc.connect("172.20.107.92", 1883, 60)

# Sending connect message
message = {
    "headerId": 0,
    "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ"),
    "version": "2.0.0",
    "manufacturer": "IC",
    "serialNumber": "0001",
    "connectionState": "ONLINE"
}

mqttc.publish("kobuki/v2/ic/0001/connection", json.dumps(message), qos=1, retain=True)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()


# Create robot instance

# receive order, create node and edge lists, pass to robot.receiveOrder function

# make step in while