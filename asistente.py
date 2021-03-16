import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import goslate
import subprocess as sub
import datetime
import mysql.connector
from difflib import SequenceMatcher as SM

listener = sr.Recognizer()
engine = pyttsx3.init()
gs = goslate.Goslate()
lista = []
voices= engine.getProperty("voices")
engine.setProperty("voices", voices[1].id)
engine.setProperty("rate", 150)
now = datetime.datetime.now()
engine.say("Hola matías")
engine.runAndWait()
rec = ""

conexion = mysql.connector.connect(host = "localhost", user = "root", passwd = "", database = "diccionario")
cursor = conexion.cursor(buffered=True)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def ejecutar():
    sub.call([r"C:/Users/Mati/Desktop/asistente/ejecutar.bat"])

def listen():
    try:
        with sr.Microphone() as source: 
            print("escuchando...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language = "es-MX")
            rec = rec.lower() 


    except:
        pass
    return rec

def chat():
    for fila in cursor:
        ide = fila[0]
        entrada = fila[1]
        salida = fila[2]
        similitud = SM(None, entrada, rec).ratio()
        print(rec)
        if similitud > 0.7:
            talk(salida)

def run():
    rec = listen() 
    if "reproduce" in rec:
        print("reproduciendo...")
        music = rec.replace("reproduce", "")
        rec = rec.replace("reproduce", "reproduciendo")
        talk(rec)
        pywhatkit.playonyt(music)
    elif "google" in rec:
        print("buscando...")
        busqueda = rec.replace("google", "")
        try:
            buqueda = busqueda.replace("busca ", "")
        except:
            pass
        try:
            busqueda = busqueda.replace("en", "")
        except:
            pass
        try:
            busqueda = busqueda.replace("in", "")
        except:
            pass
        rec = rec.replace("busca", "buscando")
        talk(rec)
        pywhatkit.search(busqueda)
    elif "wikipedia" in rec:
        order = rec.replace("wikipedia", "")
        try:
            order = order.replace("busca ", "")
        except:
            pass
        try:
            order = order.replace("en", "")
        except:
            pass
        try:
            order = order.replace("in", "")
        except:
            pass
        info = wikipedia.summary(order, 1)
        translate = gs.translate(info, "es")
        talk(translate)
    elif "abrir" and "depresión" in rec:
        rec = rec.replace("abrir", "abriendo")
        ejecutar()
    elif "enviar" in rec:
        lista = rec.split(" ")
        elementos = len(lista)
        pywhatkit.sendwhatmsg("+5493855346050","This is a message",now.hour,now.minute + 1)
        print(lista)
    
    else:
        for fila in cursor:
            ide = fila[0]
            entrada = fila[1]
            salida = fila[2]
            similitud = SM(None, entrada, rec).ratio()
            print(rec)
            if similitud > 0.7:
                talk(salida)

    


while True:
    run()


talk("Hasta pronto")