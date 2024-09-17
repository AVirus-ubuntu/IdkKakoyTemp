import datetime as dt
import logging

logging.basicConfig(filename='logs/info.log', level=logging.INFO)

users_messages = {}

class func:
    def linfo(t:str="Idk"):
        logging.info(f'{t}')
    def lwarn(t:str="Idk"):
        logging.warn(f'{t}')