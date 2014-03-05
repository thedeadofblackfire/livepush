import logging
from messenger import Messenger
#change to that for local
#from thunderpush.messenger import Messenger
import settings
#from thunderpush import settings

# add appid as apikey to have multiple domain for 1 user
# if no apikey found, try to load it dynamically from database


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

    def get_messenger_or_import_by_apikey(self, apikey):
        m = self.messengers_by_apikey.get(apikey, None)
        if not m:
            logger.info("checking apikey %s on db for instanciation", apikey)
            cnn = umysql.Connection()
            # clean user
            currentkey = apikey[4:]
            cnn.connect (settings.DB_HOST, settings.DB_PORT, settings.DB_USER, settings.DB_PASSWD, settings.DB_DB)
            rs = cnn.query("select user_id, token from ems_user where user_id = %s or token = %s", (currentkey,apikey))
            logger.info(json.dumps(rs.rows)) 
            if rs.rows:
                logger.info(json.dumps(rs.rows[0])) 
                currentkey = 'user'+str(rs.rows[0][0])
                #currentkey = str(row[1])
                logger.info(currentkey) 
                messenger = Messenger(currentkey, "1234")
                self.messengers_by_apikey[currentkey] = messenger   
                m = self.messengers_by_apikey.get(apikey, None)                
                #print "Id: %s -- Title: %s" % rs.rows[0]
                      
        return m

    def import_messenger(self):
        logger.info("Starting db %s", settings.DB_HOST)
        cnn = umysql.Connection()
        cnn.connect (settings.DB_HOST, settings.DB_PORT, settings.DB_USER, settings.DB_PASSWD, settings.DB_DB)
        rs = cnn.query("select user_id, token from ems_user where user_id != '' and token != ''")
        for i, row in enumerate(rs.rows):        
            logger.info(json.dumps(row))    
            currentkey = 'user'+str(row[0])
            #currentkey = str(row[1])
            logger.info(currentkey) 
            messenger = Messenger(currentkey, "1234")
            self.messengers_by_apikey[currentkey] = messenger            
            #self.create_messenger("%s".format(row[0]), "1234")
                   
        cnn.close()
     
