import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER', 'happyfive.eventmanager@gmail.com')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS', 'happyfive123')
    GOOGLEMAPS_KEY = os.environ.get('GOOGLEMAPS_KEY')


swagger_template = {
  "swagger": "3.0",
  "info": {
    "title": "Event Manager API ",
    "description": "API doc for Event Manager",
    "version": "0.0.1"
  },
  "consumes": [
    "application/json",
    ],
  "produces": [
    "application/json",
    ],
  "basePath": "/",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
  "operationId": "getmyData"
}


