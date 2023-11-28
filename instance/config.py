from decouple import config
# from dotenv import load_dotenv

SECRET_KEY = config("secret")
ALGORITHM = config("algorithm")
DATABASE_URL = config("database_url")