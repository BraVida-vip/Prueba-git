import os
import pytesseract
from PIL import Image
import csv

# Ruta de instalación de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# 🔧 CONFIGURACIÓN
polideportivo = "NJUL"
mes = "05"
año = "23"
carpeta_imagenes = "C:\Users\avidla\Desktop\test"  # Cambiá esta ruta
archivo_csv = "etiquetas_documentos.csv"

def extraer_texto_imagen(ruta_imagen):
    return pytesseract.image_to_string(Image.open(ruta_imagen), lang='spa')

def detectar_tipo_documento(texto):
    if "autorizacion" in texto.lower():
        return "AUT"
    elif "dni" in texto.lower():
        return "DNI"
    elif "aptitud fisica" in texto.lower():
        return "FIS"
    else:
        return "UNK"

def extraer_dni(texto):
    import re
    dni = re.findall(r'\b\d{7,8}\b', texto)
    if dni:
        return dni[0].zfill(8)
    return "00000000"

with open(archivo_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Nombre Original", "Etiqueta Generada"])

    for nombre_archivo in os.listdir(carpeta_imagenes):
        if nombre_archivo.lower().endswith(".jpg"):
            ruta_imagen = os.path.join(carpeta_imagenes, nombre_archivo)
            texto = extraer_texto_imagen(ruta_imagen)
            tipo_documento = detectar_tipo_documento(texto)
            dni = extraer_dni(texto)
            etiqueta = f"{polideportivo}_{mes}_{año}_{tipo_documento}_{dni}_01.jpg"
            writer.writerow([nombre_archivo, etiqueta])
            print(f"Procesado: {nombre_archivo} -> {etiqueta}")

print("✅ Proceso completado. Las etiquetas se guardaron en el archivo CSV.")
input("Presioná Enter para cerrar la ventana...")
