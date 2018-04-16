import os
import json
import logging

def get_database_uri():
    """
    Initialized PostgreSQL db connection
    """
    # Get the credentials from the Bluemix environment
    if 'VCAP_SERVICES' in os.environ:
        logging.info("Using VCAP_SERVICES...")
        vcap_services = os.environ['VCAP_SERVICES']
        services = json.loads(vcap_services)
        creds = services['elephantsql'][0]['credentials']
        #uri = creds["uri"]
        # username = creds["username"]
        # password = creds["password"]
        # hostname = creds["hostname"]
        # port = creds["port"]
        # name = creds["name"]
        uri = creds['uri']
    else:
        uri = 'sqlite:///db/development.db'

    logging.info("Conecting to database on %s", uri)
    # connect_string = 'mysql+pymysql://{}:{}@{}:{}/{}'
    # return connect_string.format(username, password, hostname, port, name)
    connect_string = uri
    return connect_string
