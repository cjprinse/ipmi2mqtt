from dotenv import load_dotenv
import os
load_dotenv()

IPMI_HOST = os.getenv('IPMI_HOST')
IPMI_USERNAME = os.getenv('IPMI_USERNAME')
IPMI_PASSWORD = os.getenv('IPMI_PASSWORD')
IPMI_WAIT = int(os.getenv('IMPI_WAIT') or 30)

MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = os.getenv('MQTT_PORT', 1883)
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_PREFIX = (os.getenv('MQTT_TOPIC_PREFIX') or "ipmi/"+IPMI_HOST).rstrip("/")
