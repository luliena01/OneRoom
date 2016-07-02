import psycopg2
from config import CONFIG

def connection():
    try:
        #conn = psycopg2.connect("dbname='JUNGAM' user='jungam' password='hyerim0720' host='localhost'")

        url = 'dbname=' + CONFIG['DB']['name'] + "' "
        user = 'user' + CONFIG['DB']['username'] + "' "
        password = 'password' + CONFIG['DB']['password'] + "' "
        host = 'host' + CONFIG['DB']['url'] + "' "

        print(url + user + password + host)

        conn = psycopg2.connect(url + user + password + host)

        c = conn.cursor()

        return c, conn
    except Exception as e:
        print(str(e))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

#engine = create_engine('postgresql+psycopg2://jungam:hyerim0720@localhost/JUNGAM')
engine = create_engine('postgresql+psycopg2://' + CONFIG['DB']['username'] + ':' + CONFIG['DB']['password'] + '@' + CONFIG['DB']['url'] + '/' + CONFIG['DB']['name'])
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()
