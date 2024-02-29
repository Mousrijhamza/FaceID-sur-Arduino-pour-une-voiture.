import cv2
import pickle
import serial
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Options du navigateur Chrome
options = Options()
options.add_experimental_option("detach", True)  # permet au navigateur de rester ouvert même après l'achèvement
# de toutes les opérations, conservant la fenêtre ouverte

# Initialisation du pilote Selenium Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Ouvrir notre page web
driver.get("http://127.0.0.1:5500/webpage/main.html")

# Maximiser la fenêtre du navigateur
driver.maximize_window()

# Initialiser une variable pour suivre l'état de la voiture
car_on = True

# Initialiser la connexion série
# ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)

# Configuration de la capture vidéo
video = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Chargement du détecteur de visage et des données d'entraînement dans le programme
recognise = cv2.face.LBPHFaceRecognizer_create()
recognise.read("trainner.yml")

labels = {}  # Dictionnaire pour stocker les correspondances entre ID et noms

# Ouverture du fichier "labels.pickle" et création d'un dictionnaire contenant l'ID et le nom
with open("labels.pickle", 'rb') as f:
    original_labels = pickle.load(f)
    labels = {v: k for k, v in original_labels.items()}
    print(labels)

while car_on:
    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détection des visages dans l'image en niveaux de gris
    face = cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4)

    for x, y, w, h in face:
        face_save = gray[y:y+h, x:x+w]

        # Prédiction du visage identifié
        ID, conf = recognise.predict(face_save)

        print("[" + str(ID) + ", " + str(conf) + "]")

        if 20 <= conf <= 80:
            # print(ID)
            # print(labels[ID])

            if labels[ID] in {'hamza', 'hamzabouiri', 'hamza_bouiri', 'HamzaMousrij', 'hamza_buiri', 'oussama'}: #les personne que le modele approuve a demarer la voiture
                # ser.write(b'1')
                cv2.putText(frame, labels[ID], (x-10, y-10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)

                if car_on:
                    try:
                        # Attendre que le bouton soit cliquable
                        button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.ID, "stopButton"))
                        )
                        # Cliquer sur le bouton
                        button.click()
                        car_on = False
                    except Exception as e:
                        print(f"Erreur lors du clic sur le bouton : {e}")

            else:
                cv2.putText(frame, "Inconnu", (x-10, y-10), cv2.FONT_HERSHEY_COMPLEX, 1, (18, 5, 255), 2, cv2.LINE_AA)
                frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 4)
                # ser.write(b'0')

                if not car_on:
                    try:
                        # Attendre que le bouton soit cliquable
                        button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.ID, "stopButton"))
                        )
                        # Cliquer sur le bouton
                        button.click()
                        car_on = True
                    except Exception as e:
                        print(f"Erreur lors du clic sur le bouton : {e}")

    # Afficher la vidéo avec les visages détectés
    cv2.imshow("Vidéo", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Fermer la connexion série et libérer la capture vidéo
#ser.close()
video.release()
cv2.destroyAllWindows()
