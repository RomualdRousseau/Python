import os
import json                                                                
import paho.mqtt.client as mqtt                                          
import redis                                                             
import function                                                                    

MQTT_HOST = os.environ['MQTT_HOST']                                      
MQTT_USERNAME = os.environ['MQTT_USERNAME']                              
MQTT_PASSWORD = os.environ['MQTT_PASSWORD']

REDIS_HOST = os.environ['REDIS_HOST']                                    
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

DATA_PATH = "/var/blob/data"
                                                                         
r = redis.Redis(host = REDIS_HOST, password = REDIS_PASSWORD)            
m = mqtt.Client() 

def setup():                                                                         
    m.on_connect = on_connect                                                
    m.on_message = on_message                                                
    m.username_pw_set(username = MQTT_USERNAME, password = MQTT_PASSWORD)
    m.connect(MQTT_HOST, 1883, 60)  

def loop():
    m.loop_forever()

def on_connect(client, userdata, flags, rc):                             
    if rc==0:                                                        
        print("Connected OK")                  
        client.subscribe("blob.in.watcher") 
        print("Suscribed to topic blob.in.watcher")               
    else:                                                            
        print("Bad connection Returned code=", rc)                
                                                                         
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    payload = json.loads(msg.payload)

    if "in" in payload["file_name"].upper():
        function.run(DATA_PATH + "/" + payload["file_name"], DATA_PATH + "/out.csv")
        client.publish("blob.out.watcher", "{ \"file_name\": \"out.csv\"}")

if __name__ == "__main__":
    setup()
    loop()
