import os

from dotenv import load_dotenv

load_dotenv()

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
database = os.environ['POSTGRES_DB']

connection_uri = f'postgresql://{user}:{password}@localhost:5433/{database}'
