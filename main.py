import pyipmi.interfaces
from pyipmi.errors import IpmiTimeoutError

import settings
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:

        print("Connected to broker")

        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed")

def ipmiControl(topic, payload):
    if topic.endswith('set_power_state'):
        global ipmi
        ipmi.chassis_control(int(payload))
        print('Set power state:', payload)
    elif topic.endswith('set_power_soft'):
        if payload == '1':
            ipmi.chassis_control_power_up()
        else:
            ipmi.chassis_control_soft_shutdown()
        print('Set power:', payload)

def on_message(client, userdata, message):
    topic = str(message.topic)
    payload = str(message.payload.decode("utf-8"))
    print("Received:", topic, "=", payload)

    try:
        ipmiControl(topic, payload)
    except Exception as e:
        try:
            ipmi.session.establish()
            ipmiControl(topic, payload)
        except Exception as eNested:
            print('Cannot set power state:', eNested)


Connected = False
ipmi = None

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    interface = pyipmi.interfaces.create_interface(interface='rmcp',
                                                   slave_address=0x81,
                                                   host_target_address=0x20,
                                                   keep_alive_interval=1)
    global ipmi
    ipmi = pyipmi.create_connection(interface)
    ipmi.session.set_session_type_rmcp(host=settings.IPMI_HOST, port=623)
    ipmi.session.set_auth_type_user(username=settings.IPMI_USERNAME, password=settings.IPMI_PASSWORD)
    ipmi.target = pyipmi.Target(ipmb_address=0x20)
    ipmi.session.establish()

    mqttPrefix = settings.MQTT_PREFIX + '/'

    mqttClient = mqtt.Client()
    if (settings.MQTT_USERNAME):
        mqttClient.username_pw_set(settings.MQTT_USERNAME, password=settings.MQTT_PASSWORD)  # set username and password

    mqttClient.on_connect = on_connect
    mqttClient.connect(settings.MQTT_HOST, settings.MQTT_PORT)
    mqttClient.subscribe(mqttPrefix+'set_power_state')
    mqttClient.subscribe(mqttPrefix+'set_power_soft')
    mqttClient.on_message = on_message
    mqttClient.loop_start()

    while Connected != True:  # Wait for connection
        time.sleep(0.1)

    while True:

        try:
            print(ipmi.get_device_sdr_list())
            print('Read sdr list')
        except Exception as e:
            print('Cannot read ipmi sensors:', e)

        try:
            mqttClient.publish(
                mqttPrefix + 'power_on',
                1 if ipmi.get_chassis_status().power_on else 0,
                0,
                True
            )
        except Exception as e:
            print('Cannot publish power state:', e)
            break

        time.sleep(settings.IPMI_WAIT)

    ipmi.session.close()
    print('IPMI disconnected')

    mqttClient.disconnect()
    mqttClient.loop_stop()
    print('mqtt disconnected')
