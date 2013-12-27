#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import with_statement

import time
import datetime
import logging
import umysql

logger = logging.getLogger()

try:
    import simplejson as json
except ImportError:
    import json # NOQA
    
#logger = logging.getLogger(__name__)
#if True and settings.VERBOSE:
#if True:
    #logger.setLevel(logging.DEBUG)
    #logger_hdlr = logging.StreamHandler()
    #logger_hdlr.setFormatter(logging.Formatter(fmt="HTTP server: %(message)s"))
    #logger.addHandler(logger_hdlr)
    #logger_filehdlr = logging.FileHandler(format(settings.PATH_DIRECTORY_LOG) + 'vico_' + datetime.now().strftime("%Y%m%d") + '.log')
    #logger_filehdlr.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - HTTP server: %(message)s'))
    #logger.addHandler(logger_filehdlr)

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWD = ''
DB_DB = 'textapp'   

'''                      
def run_app():
    # configure logging level
    if settings.VERBOSE:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
'''

def testConnectWithNoDB():
    logger.info("Starting db %s", DB_HOST)
    cnn = umysql.Connection()
    cnn.connect (DB_HOST, DB_PORT, DB_USER, DB_PASSWD, DB_DB)
    rs = cnn.query("select user_id, token from ems_user")
    for i, row in enumerate(rs.rows):   
        logger.info(json.dumps(row)) 
        
    cnn.close()
        
class Db:
    
    def __init__(self):     
        self.salt = None
        
    def testConnectWithNoDB(self):
        logger.info("Starting db")
        cnn = umysql.Connection()
        cnn.connect (settings.DB_HOST, settings.DB_PORT, DB_USER, DB_PASSWD, DB_DB)
        rs = cnn.query("select user_id, token from ems_user")
        for i, row in enumerate(rs.rows):   
            logger.info(json.dumps(row)) 
        
        cnn.close()

'''
def main():

    run_app()
    testConnectWithNoDB()    
    #Db().testConnectWithNoDB();
    

if __name__ == "__main__":
    main()
'''