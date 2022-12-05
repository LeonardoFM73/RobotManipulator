import paho.mqtt.client as mqtt #import library
import paho.mqtt.publish as publish
import cv2
 
MQTT_SERVER = "localhost" #specify the broker address, it can be IP of raspberry pi or simply localhost
MQTT_PATH = "test_channel" #this is the name of topic, like temp

found = False
input1 = ""
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if str(msg.payload) == "b'Run'":
        found = True
    while found is True:
        inp=input("Deteksi:")
        #inp=deteksi()
        publish.single(MQTT_PATH, inp, hostname=MQTT_SERVER)

def deteksi():
            # set up camera object
    global input1
    cap = cv2.VideoCapture(0)

    # QR code detection object
    detector = cv2.QRCodeDetector()

    while True:
        found = False
        # get the image
        _, img = cap.read()
        # get bounding box coords and data
        data, bbox, _ = detector.detectAndDecode(img)
        
        # if there is a bounding box, draw one, along with the data
        if(bbox is not None):
            for i in range(len(bbox)):
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                         0, 255), thickness=2)
            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
            if data:
                input1 =data
                if data is "Biru" or data is "Merah" or data is "Hijau" or data is "Kuning":  
                    print("data found: ", data)
                    found = True
        # display the image preview
        cv2.imshow("code detector", img)
        if(cv2.waitKey(1) == ord("q")) or found is True:
            break
    # free camera object and exit
    cap.release()
    cv2.destroyAllWindows()
    return input1
    
    # more callbacks, etc
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)


client.loop_forever()# use this line if you don't want to write any further code. It blocks the code forever to check for data
#client.loop_start()  #use this line if you want to write any more code here

