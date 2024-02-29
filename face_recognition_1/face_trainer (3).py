# Importation des bibliothèques requises
import cv2
import os
import numpy as np
from PIL import Image
import pickle

# Chargement du classificateur en cascade pour la détection de visages
cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Création d'un objet de reconnaissance faciale basé sur l'algorithme LBPH
recognise = cv2.face.LBPHFaceRecognizer_create()

#fonction
def getdata():

    current_id = 0
    label_id = {}  # Dictionnaire
    face_train = []  # Liste 
    face_label = []  # Liste 
    
    # Rechercher l'emplacement de fichier "image_data" contenant les données
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    my_face_dir = os.path.join(BASE_DIR,'image_data')

    # Recherche de tous les dossiers et fichiers à l'intérieur du dossier "image_data" a l'extension ".png" ou ".jpg"
    for root, dirs, files in os.walk(my_face_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                # Ajout du chemin du fichier avec le chemin de base pour obtenir le chemin de l'image 
                path = os.path.join(root, file)

                # libeller en récupérant le nom du dossier 
                label = os.path.basename(root).lower()

                # Attribution d'un identifiant unique à chaque personne
                if not label in label_id:
                    label_id[label] = current_id
                    current_id += 1
                ID = label_id[label]

                # Conversion de l'image en niveaux de gris
                pil_image = Image.open(path).convert("RGB") 

                # Conversion des données de l'image en tableau numpy
                image_array = np.array(pil_image, "uint8")
        
                # Détection des visages dans l'image
                face = cascade.detectMultiScale(image_array)

                # Recherche de la région d'intérêt (ROI) et ajout des données correspondantes
                for x, y, w, h in face:
                    img = image_array[y:y+h, x:x+w]
                    cv2.imshow("Test", img)  # Affichage de l'image avec le visage encadré (optionnel)
                    cv2.waitKey(1)
                    face_train.append(img)
                    face_label.append(ID)

    # Stockage des données d'étiquettes, Ce fichier est créé pour stocker
    #  les correspondances entre les noms des personnes (étiquettes) et leurs identifiants uniques
    with open("labels.pickle", 'wb') as f:
        pickle.dump(label_id, f)
   
    return face_train, face_label

# Après avoir extrait les visages et attribué des étiquettes, le script utilise ces 
# données pour entraîner un modèle de reconnaissance faciale à l'aide de 
# l'algorithme LBPH (Local Binary Pattern Histograms).
# afin de sauvgarder dans un fichier ".yml"
face, ids = getdata()
recognise.train(face, np.array(ids))
recognise.save("trainner.yml")
