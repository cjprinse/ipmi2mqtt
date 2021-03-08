# ipmi2mqtt
Connector to power control ipmi server via mqtt

## Environment variables (also located in .env.dist)
IPMI_HOST=
IPMI_USERNAME=
IPMI_PASSWORD=
IPMI_WAIT=timeout in seconds to rerun statistics, default to 30

MQTT_HOST=
MQTT_PORT=default to 1883
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_PREFIX=Topic prefix, default to ipmi/{MQTT_HOST}

## MQTT topics
* Power state is published to {MQTT_PREFIX}/power_on (retained)
* Power state can be set via topic {MQTT_PREFIX}/set_power_state
