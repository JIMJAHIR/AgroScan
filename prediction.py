from flask import Flask, render_template, request
import os
import numpy as np
from PIL import Image
import tensorflow as tf
import cv2  # Agregar esta línea

app = Flask(__name__)

# ia_coffe

imagen_alto, imagen_ancho = 150, 300
model = tf.keras.models.load_model('ia_coffe.h5')

def preprocess_image(image):
    image = image.resize((imagen_ancho, imagen_alto))
      
    return image


imagen_altot, imagen_anchot = 200, 200
modelT = tf.keras.models.load_model('ia_tomato.h5')

def preprocess_tomato(image):
    image = image.resize((imagen_anchot, imagen_altot))
      
    return image


imagen_altoc, imagen_anchoc = 200, 200
modelM = tf.keras.models.load_model('ia_maiz.h5')

def preprocess_corn(image):
    image = image.resize((imagen_anchoc, imagen_altoc))
      
    return image


imagen_altor, imagen_anchor = 300, 300
modelR = tf.keras.models.load_model('ia_rice.h5')

def preprocess_rice(image):
    image = image.resize((imagen_anchor, imagen_altor))
      
    return image


# Función para realizar la predicción
def predict_coffe(image):
    preprocessed_image = preprocess_image(image)
    normalizar = np.array(preprocessed_image) / 255.0
    input_batch = np.expand_dims(np.array(normalizar), axis=0)
    prediction = model.predict(input_batch)
    
    # Decodificar la predicción en una etiqueta (por ejemplo, 'miner', 'nodisease', ...)
    labels = ['Miner', 'Hoja Sana', 'Phoma', 'Rust']
    predicted_label = labels[np.argmax(prediction)]

    return predicted_label


# Función para realizar la predicción
def predict_tomato(image):
    preprocessed_image = preprocess_tomato(image)
    normalizar = np.array(preprocessed_image) / 255.0
    input_batch = np.expand_dims(np.array(normalizar), axis=0)
    prediction = modelT.predict(input_batch)
    
    # Decodificar la predicción en una etiqueta (por ejemplo, 'miner', 'nodisease', ...)
    labels = ['Mancha Bateriana','Tizón Temprano','Saludable','Tizón Tardio',
              'Molde Hoja','Septoria','Acaros de Araña','Punto Objetivo','Virus Mosaico','Tomate Amarillo']
    predicted_label = labels[np.argmax(prediction)]

    return predicted_label


# Función para realizar la predicción
def predict_corn(image):
    preprocessed_image = preprocess_corn(image)
    normalizar = np.array(preprocessed_image) / 255.0
    input_batch = np.expand_dims(np.array(normalizar), axis=0)
    prediction = modelM.predict(input_batch)
    
    # Decodificar la predicción en una etiqueta (por ejemplo, 'miner', 'nodisease', ...)
    labels = ['Common_Rust','Gray_Leaf_Spot','Saludable','Blight']
    predicted_label = labels[np.argmax(prediction)]

    return predicted_label


# Función para realizar la predicción
def predict_rice(image):
    preprocessed_image = preprocess_rice(image)
    normalizar = np.array(preprocessed_image) / 255.0
    input_batch = np.expand_dims(np.array(normalizar), axis=0)
    prediction = modelR.predict(input_batch)
    
    # Decodificar la predicción en una etiqueta (por ejemplo, 'miner', 'nodisease', ...)
    labels = ['bacterial_leaf_blight', 'brown_spot', 'healthy', 'leaf_blast', 'leaf_scald', 'narrow_brown_spot']
    predicted_label = labels[np.argmax(prediction)]

    return predicted_label


if __name__ == '__main__':
    app.run(debug=True)