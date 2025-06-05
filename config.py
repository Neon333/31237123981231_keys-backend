import os
from dotenv import load_dotenv


load_dotenv()


script_dir = os.path.dirname(os.path.abspath(__file__))
IMAGE_HOST_PATH = os.path.join(script_dir, os.getenv('IMAGE_HOST_PATH'))
FREEKASSA_API_KEY = os.getenv('FREEKASSA_API_KEY')
FREEKASSA_SECRET_1 = os.getenv('FREEKASSA_SECRET_1')
FREEKASSA_SECRET_2 = os.getenv('FREEKASSA_SECRET_2')
FREEKASSA_MERCHANT_ID = os.getenv('FREEKASSA_MERCHANT_ID')  #__

CRYSTALPAY_LOGIN = ''
CRYSTALPAY_SECRET = ''
CRYSTALPAY_SALT = ''


WEBSITE_DOMAIN = os.getenv('WEBSITE_DOMAIN')
PAYMENTS_WEBHOOK_URL = WEBSITE_DOMAIN + '/api' +os.getenv('PAYMENTS_WEBHOOK_URL')