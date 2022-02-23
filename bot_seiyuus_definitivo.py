from logging import error
import tweepy
import os
import shutil
import random
from dotenv import load_dotenv


class diosa:
    
    # Constructor
    def __init__(self, consumer_key, consumer_secret, key, secret, tweet, pics_dir, used_pics):
        self.consumer_key = consumer_key  # La consumer key para la api de tw
        self.consumer_secret = consumer_secret  # La consumer secret para la api de tw
        self.key = key  # La key para la api de tw
        self.secret = secret  # La secret para la api de tw
        self.tweet = tweet  # El texto del tweet
        self.pics_dir = pics_dir  # El nombre del directorio donde estan guardadas las imagenes
        self.used_pics_directory = used_pics  # El directorio donde van las imagenes usadas


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


    # Metodo para quitar del directorio la imagen
    def deleteUsedImage(self):
        pics = self.initPicsDirectory()  # variable para iniciar la lista de fotos
        # variable para crear la path de la imagen]
        path_actual = self.pics_dir + '/' + self.randomImage()

    # Metodo para twitear

    def tweetPic(self):
        try:
            pics = self.initPicsDirectory()  # variable para iniciar la lista de fotos
            api = self.auth()  # variable de la api de twitter
            # variable para crear la path de la imagen
            path_actual = self.pics_dir + '/' + random.choice(pics)
            destination = self.used_pics_directory
            # metodo para poner el tweet con imagen de la path actual y el tweet guardado en el objeto
            api.update_with_media(path_actual, status=self.tweet)
            shutil.move(path_actual, destination)
        except:
            print("Ha pasao algo que seguramente te va a poner de mala hostia, pero ntr mi pana, ponte un poquito de Reigning de fondo y lo solucionas ez")
            print(error)

    # Metodo para hacer todo el proceso de hacer el a guardar la lista de imagenes, twitear y pasar a la siguiente imagen.

    def fullProcess(self):
        self.auth()
        self.initPicsDirectory()
        self.tweetPic()


def main():
    load_dotenv()
    reochi = diosa(os.getenv('consumer_key_reochi'), os.getenv('consumer_secret_reochi'),os.getenv('key_reochi'),
            os.getenv('secret_reochi'), "#倉知玲鳳 #KurachiReo", 'diosa', "imagenes usadas reochi")
    yukki = diosa(os.getenv('consumer_key_yukki'), os.getenv('consumer_secret_yukki'),os.getenv('key_yukki'),
            os.getenv('secret_yukki'), "#中島由貴 #NakashimaYuki", 'diosa yukki', "imagenes usadas yukki")
    himaringo = diosa(os.getenv('consumer_key_himaringo'), os.getenv('consumer_secret_himaringo'),os.getenv('key_himaringo'),
            os.getenv('secret_himaringo'), "#葉月ひまり #HazukiHimari", 'imagenes himaringo', 'imagenes usadas himaringo' )
    hachan = diosa(os.getenv('consumer_key_hachan'), os.getenv('consumer_secret_hachan'),os.getenv('key_hachan'),
            os.getenv('secret_hachan'), "#反田葉月 #TandaHazuki", 'imagenes hachan', 'imagenes usadas hachan')
    
    yukki.fullProcess()
    reochi.fullProcess()
    himaringo.fullProcess()
    hachan.fullProcess()


if __name__ == "__main__":
    print("VAMO VOLANDO NINHO")
    main()
