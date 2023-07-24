import os
import random
import string
import tempfile
import pandas as pd
from faker import Faker
from io import BytesIO
from pyDataverse.api import NativeApi
from pyDataverse.models import Dataset, Datafile
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from PIL import Image

# Remplacer BASE_URL et API_TOKEN par vos informations
BASE_URL = "YOUR_BASE_URL_HERE"
API_TOKEN = "YOUR_API_TOKEN_HERE"

# Créer une instance NativeApi
api = NativeApi(BASE_URL, API_TOKEN)

# Remplacer DOI par le DOI du Dataset existant
DOI = "doi:10.5072/FK2/EO7BNB"

# Fonction pour générer un fichier texte aléatoire de taille comprise entre 500 Ko et 1 Mo
def generate_random_text_file():
    fake = Faker()
    filename = fake.file_name(extension="txt")
    content = fake.text(max_nb_chars=random.randint(500, 1024) * 1024)  # Entre 500 Ko et 1 Mo
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

# Fonction pour générer un fichier JPG aléatoire de taille comprise entre 500 Ko et 1 Mo
def generate_random_jpg_file():
    fake = Faker()
    filename = fake.file_name(extension="jpg")
    # Générer une image JPG aléatoire
    image = Image.new("RGB", (800, 600), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    image.save(filename)
    return filename

# Fonction pour générer un fichier CSV aléatoire de taille comprise entre 500 Ko et 1 Mo
def generate_random_csv_file():
    fake = Faker()
    filename = fake.file_name(extension="csv")
    # Générer un dataframe pandas avec des données aléatoires
    num_rows = random.randint(500, 1024)  # Entre 500 Ko et 1 Mo
    df = pd.DataFrame({'Colonne1': [fake.name() for _ in range(num_rows)],
                       'Colonne2': [fake.email() for _ in range(num_rows)],
                       'Colonne3': [fake.random_int(0, 100) for _ in range(num_rows)]})
    df.to_csv(filename, index=False)
    return filename

# Fonction pour envoyer un fichier dans le Dataset via l'API de Dataverse
def upload_file_to_dataset(dataset_pid, file_path):
    datafile = Datafile()
    datafile.set({"pid": dataset_pid, "filename": os.path.basename(file_path)})
    with open(file_path, "rb") as f:
        resp = api.upload_datafile(dataset_pid, os.path.basename(file_path), datafile.json(), f.read())
        if resp.status_code == 200:
            print(f"Le fichier {os.path.basename(file_path)} a été déposé avec succès dans le Dataset.")
        else:
            print(f"Une erreur est survenue lors du dépôt du fichier {os.path.basename(file_path)}.")

# Créer une instance Dataset en utilisant le DOI du Dataset existant
dataset = api.get_dataset(DOI)

# Générer et envoyer des fichiers aléatoires dans le Dataset
print("Génération et envoi de fichiers aléatoires dans le Dataset en cours...")
for i in range(5):  # Générer et envoyer 5 fichiers aléatoires
    print(f"Génération du fichier aléatoire n°{i+1}...")
    file_type = random.choice(["txt", "jpg", "csv"])
    if file_type == "txt":
        file_path = generate_random_text_file()
    elif file_type == "jpg":
        file_path = generate_random_jpg_file()
    elif file_type == "csv":
        file_path = generate_random_csv_file()

    print(f"Envoi du fichier aléatoire n°{i+1} dans le Dataset...")
    upload_file_to_dataset(DOI, file_path)

    # Supprimer le fichier temporaire après l'envoi
    os.remove(file_path)

print("Tous les fichiers aléatoires ont été générés et déposés dans le Dataset.")
