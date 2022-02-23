from logging import error
import tweepy
import os
import schedule
import time
import shutil
import random


class diosa:
    # Constructor
    def __init__(self, consumer_key, consumer_secret, key, secret, tweet, counterFile, pics_dir, actual_pic, used_pics):
        self.consumer_key = consumer_key  # La consumer key para la api de tw
        self.consumer_secret = consumer_secret  # La consumer secret para la api de tw
        self.key = key  # La key para la api de tw
        self.secret = secret  # La secret para la api de tw
        self.tweet = tweet  # El texto del tweet
        # El nombre del archivo txt para hacer el recuento de imagenes
        self.counterFile = counterFile
        self.pics_dir = pics_dir  # El nombre del directorio donde estan guardadas las imagenes
        # Un entero que guarda el iterador de la imagen por la que va
        self.actual_pic = actual_pic
        # El directorio donde van las imagenes usadas
        self.used_pics_directory = used_pics

    # Metodo para autentificarse en twitter
    def auth(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.key, self.secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api  # Retorna la api para poder usarla para poner luego el tweet

    # Metodo para hacer una lista con las imagenes disponibles en el directorio correspondiente
    def initPicsDirectory(self):
        pics = []  # lista vacia para guardar las imagenes
        # Metodo de la clase 'os' para hacer una lista de todo el contenido de un directorio
        content = os.listdir(self.pics_dir)
        # Bucle for para guardar todas las paths de las fotos en la lista
        for fichero in content:
            if os.path.isfile(os.path.join(self.pics_dir, fichero)):
                pics.append(fichero)
        return pics  # El metodo devuelve la lista de las imagenes

    # Metodo para leer el archivo txt para saber por que foto se va iterando
    def readIteratorFile(self):
        i = 0  # iterador
        # metodo para abrir el archivo
        archivoLectura = open(self.counterFile, "r")
        linea = archivoLectura.readline()  # metodo para leer la primera linea del archivo
        # guardamos lo que hay en la linea del archivo en una variable
        i = int(linea)
        archivoLectura.close()  # cerramos el archivo para evitar cosas raras
        self.actual_pic = i  # seteamos la imagen actual en el objeto

    # Metodo para sobreescribir el archivo que hace la cuenta de las fotos, recibe un entero para escribirlo en el archivo txt
    def writeIteratorFile(self, i):
        archivoMod = open(self.counterFile, "w")  # abrimos el archivo txt
        # le sumamos uno al valor que recivimos y lo guardamos en la variable que lleva el conteo
        self.actual_pic = i+1
        # escribimos en el archivo txt la variable convertida a string
        archivoMod.write(str(self.actual_pic))
        archivoMod.close()  # cerramos el archivo para evitar errores

    # Metodo para quitar del directorio la imagen

    def deleteUsedImage(self):
        self.readIteratorFile()
        pics = self.initPicsDirectory()  # variable para iniciar la lista de fotos
        path_actual = self.pics_dir + '/' + pics[self.actual_pic] ## variable para crear la path de la imagen]
        destination = self.used_pics_directory
        shutil.move(path_actual, destination)


    # Metodo para twitear
    def tweetPic(self):
        try:
            pics = self.initPicsDirectory() ## variable para iniciar la lista de fotos
            api = self.auth() ## variable de la api de twitter
            path_actual = self.pics_dir + '/' + pics[self.actual_pic] ## variable para crear la path de la imagen
            api.update_with_media(path_actual, status=self.tweet) ## metodo para poner el tweet con imagen de la path actual y el tweet guardado en el objeto
            self.writeIteratorFile(self.actual_pic) ## Sobreescribimos el archivo txt del iterador
        except:
            print("Ha pasao algo que seguramente te va a poner de mala hostia, pero ntr mi pana, ponte un poquito de Reigning de fondo y lo solucionas ez")


    # Metodo para hacer todo el proceso de hacer el a guardar la lista de imagenes, twitear y pasar a la siguiente imagen.
    def fullProcess(self):
        self.auth()
        self.initPicsDirectory()
        self.readIteratorFile()
        self.tweetPic()
        self.deleteUsedImage()


def main():
    reochi = diosa('n5IqvPl1XIlcAQtgOghIorW9T', 'wVAjG4mFA6ORKBHloNIYobIy41oBmVZ8acsFICK7e2yqMIKeoY','1438078965692911617-m0VhIjXfS21gBtuuNPoKrHsDJ620RI',
    '2LHxP3Tlc3wgJIIEuso0xkaptml193YW7mhj2ct4Hkjfp', "#倉知玲鳳 #KurachiReo", "reochiCounter.txt", 'diosa', 5, "imagenes usadas reochi")
    yukki = diosa('pr8Yu0qQOozXKfs6A33UHaNYW', 'M7xlGwWEgv7qVdyQedY01Xfh72Pq5g345JA4hDWLpIWDCghxjO', '1438501509876961280-VA5S8ewoUeM7z5dKh1Xb3jGMUD2elg',
    'IjfG3AZYAGr65ci3BKdWPD02l5YVmg7aDYDEcSvlS3Ik8', "#中島由貴 #NakashimaYuki", "yukkiCounter.txt", 'diosa yukki', 3, "imagenes usadas yukki")
    schedule.every().day.at("20:00").do(yukki.fullProcess)
    schedule.every().day.at("20:00").do(reochi.fullProcess)
    reochi.deleteUsedImage()
    while True:
        try:
            schedule.run_pending()
            time.sleep(2)
        except tweepy.TweepError as e:
            raise e

  
if __name__ == "__main__":
    print("VAMO VOLANDO NINHO")
    main()
