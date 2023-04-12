import os

class Config(object):
  SECRET_KEY = "my_secret_key"
  MAIL_SERVER = 'smtp.gmail.com'
  MAIL_PORT = 465
  MAIL_USE_SSL = False
  MAIL_USE_TSL = True
  MAIL_USERNAME = 'juandmatos0014@gmail.com'
  MAIL_PASSWORD = 'Emanuel17'
  
class DevelopmentConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:30000/flask'