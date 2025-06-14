import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import time
import serial
import requests

# Chargement du modèle
model = load_model("keras_Model.h5", compile=False)

# Chargement des labels
class_names = open("labels.txt", "r").readlines()

# Démarrage de la webcam
cap = cv2.VideoCapture(0)

#permet d'envoyer les données sur Arduino
arduino_port = '/dev/tty.usbmodem1201'
baud_rate = 9600

# Ouvre la connexion série
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # Laisse le temps à Arduino de redémarrer

# Variables de comptage
count_class_1 = 0
count_class_2 = 0
count_class_3 = 0

# ThingsBoard settings
THINGSBOARD_TOKEN = ""
THINGSBOARD_URL = "https://demo.thingsboard.io/api/v1/" + THINGSBOARD_TOKEN + "/telemetry"

def send_to_thingsboard(c1, c2, c3):
    payload = {
        "count_class_1": c1,
        "count_class_2": c2,
        "count_class_3": c3
    }
    try:
        response = requests.post(THINGSBOARD_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print("[ThingsBoard] Données envoyées avec succès")
        else:
            print(f"[ThingsBoard] Erreur HTTP : {response.status_code}")
    except Exception as e:
        print(f"[ThingsBoard] Exception : {e}")

while True:
    # Capture image webcam
    ret, frame = cap.read()
    if not ret:
        print("Erreur de capture")
        break

    # Traitement image
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) #conversion de l'img en RGB
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS) #redimensionne l'image
    image_array = np.asarray(image) #conversion de l'image en un tableau
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1 #Normalisation des données images pour avoir les valeuresentre -1 et 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32) #création d'un tableau avec les params attendus
    data[0] = normalized_image_array

    # Prédiction
    prediction = model.predict(data) #prédiction de l'image d'appartenir à une classe
    index = np.argmax(prediction) #trouve la classe avec la plus forte proba
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index] #récupération de la proba

    # Comptage des classes si confiance > 60%
    if confidence_score > 0.6:
        if index == 0:
            count_class_1 += 1
        elif index == 1:
            count_class_2 += 1
        elif index == 2:
            count_class_3 += 1

        class_number = index + 1
        ser.write(f"{class_number}\n".encode('utf-8'))
        print(f"[PC → Arduino] Classe envoyée : {class_number}")
        print(f"Compteurs -> Classe 1: {count_class_1}, Classe 2: {count_class_2}, Classe 3: {count_class_3}")

        # Envoi vers ThingsBoard
        send_to_thingsboard(count_class_1, count_class_2, count_class_3)

    # Affichage
    label = f"{class_name} ({confidence_score * 100:.2f}%)"
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Webcam - Press Q to quit", frame)

    # Sortie avec Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(2)  # Réduction à 0.5s pour un flux plus fluide

# Nettoyage
cap.release()
cv2.destroyAllWindows()
ser.close()
