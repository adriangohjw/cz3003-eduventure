POSTGRES_USER = 'postgres'
POSTGRES_PW = 'localhostdbpassword'
POSTGRES_URL = '127.0.0.1:5432'
POSTGRES_DB = 'cz3003'

class Config:
    URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)