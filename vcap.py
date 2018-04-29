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
        uri = creds['uri']
    else:
        uri = 'postgres://postgres:passw0rd@localhost:5432/test'

    logging.info("Conecting to database on %s", uri)
    connect_string = uri
    return connect_string
