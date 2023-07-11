from os import getenv
from dotenv import load_dotenv

def cargar_variables():
    """ Carga las variables del archivo .env """
    load_dotenv()


if __name__ == "__main__":
    cargar_variables()