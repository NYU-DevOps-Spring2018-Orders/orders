"""
VCAP Services module
This module initializes the database connection String
from VCAP_SERVICES in Bluemix if Found
"""

import os
import json
import logging


def get_database_uri():
    """
    Initialized MySQL database connection
    This method will work in the following conditions:
      1) In Bluemix with MySQL bound through VCAP_SERVICES
      2) With MySQL running on the local server as with Travis CI
      3) With MySQL --link in a Docker container called 'mariadb'
    """
    # Get the credentials from the Bluemix environment
    if 'VCAP_SERVICES' in os.environ:
        logging.info("Using VCAP_SERVICES...")
        vcap_services = os.environ['VCAP_SERVICES']
        services = json.loads(vcap_services)
        creds = services['cleardb'][0]['credentials']
        username = creds["username"]
        password = creds["password"]
        hostname = creds["hostname"]
        port = creds["port"]
        name = creds["name"]
    elif 'TRAVIS' in os.environ:
        logging.info("Using Travis...")
        username = 'root'
        password = ''
        hostname = 'localhost'
        port = '3306'
        name = 'development'
    else:
        logging.info("Using localhost database...")
        username = 'root'
        password = 'passw0rd'
        hostname = 'localhost'
        port = '3306'
        name = 'development'

    logging.info("Connecting to database on host %s port %s", hostname, port)
    connect_string = 'mysql+pymysql://{}:{}@{}:{}/{}'
    return connect_string.format(username, password, hostname, port, name)