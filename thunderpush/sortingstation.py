import logging
from messenger import Messenger
#change to that for local
#from thunderpush.messenger import Messenger
import settings
#from thunderpush import settings


logger = logging.getLogger()


import umysql

try:
    import simplejson as json
except ImportError:
    import json # NOQA

class SortingStation(object):
    """ Handles dispatching messages to Messengers. """

    _instance = None

    def __init__(self, *args, **kwargs):
        if self._instance:
            raise Exception("SortingStation already initialized.")

        self.messengers_by_apikey = {}

        SortingStation._instance = self

    @staticmethod
    def instance():        
        return SortingStation._instance

    def create_messenger(self, apikey, apisecret):
        messenger = Messenger(apikey, apisecret)

        self.messengers_by_apikey[apikey] = messenger

    def delete_messenger(self, messenger):
        del self.messengers_by_apikey[messenger.apikey]

    def get_messenger_by_apikey(self, apikey):
        return self.messengers_by_apikey.get(apikey, None)

    def import_messenger(self):
        logger.info("Starting db %s", DB_HOST)
        cnn = umysql.Connection()
        cnn.connect (DB_HOST, DB_PORT, DB_USER, DB_PASSWD, DB_DB)
        rs = cnn.query("select user_id, token from ems_user where user_id != '' and token != ''")
        for i, row in enumerate(rs.rows):        
            logger.info(json.dumps(row))     
            #logger.info(json.dumps(row[0]))  
            messenger = Messenger(row[0], "1234")
            self.messengers_by_apikey[row[0]] = messenger            
            #self.create_messenger("%s".format(row[0]), "1234")
                   
        cnn.close()
     
