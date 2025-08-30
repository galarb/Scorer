# mqttReceiver.py
import json
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion

MQTT_BROKER = "10.100.102.47"   # your Pi's IP
MQTT_PORT   = 1883
MQTT_TOPIC  = "control/vector"

class MqttReceiver:
    def __init__(self, scorer):
        self.scorer = scorer
        self.client = mqtt.Client(
            client_id="scorer",
            callback_api_version=CallbackAPIVersion.VERSION2
        )
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def start(self):
        self.client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print("MQTT connected:", reason_code)
        client.subscribe(MQTT_TOPIC, qos=0)

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            #print(data)
            vx = int(data.get("vx", 0))
            vy = int(data.get("vy", 0))
            omega = int(data.get("omega", 0))
            dribbler = int(data.get("dribbler", 0))
            kick = int(data.get("kick", 0))

            # ✅ Only act if robot is in MANUAL mode (modeflag == 2)
            if self.scorer.get_modeflag() == 2:
                print(data)
                self.scorer.govector(vx, vy, omega)

                if dribbler:
                    self.scorer.dribbler.motgo(60)
                else:
                    self.scorer.dribbler.motgo(0)

                if kick:
                    self.scorer.kick()

        except Exception as e:
            print("Error processing MQTT:", e)

