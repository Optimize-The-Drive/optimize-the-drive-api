import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__name__))
dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)


DATABASE_URL = "postgres://{user}:{password}@{host}:{port}/{database}".format(
        user=os.getenv('DB_USER', 'root'),
        password=password,
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_DATABASE'),
)
