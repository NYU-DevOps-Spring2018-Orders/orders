"""
Order Service Runner
Starts the Order service and initializes logging
"""

import os
from app import app, server

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')


######################################################################
# MAIN
######################################################################
if __name__ == "__main__":
    print "========================================="
    print " ORDERS SERVICE STARTING"
    print "========================================="
    server.initialize_logging()
    server.init_db()  # make our sqlalchemy tables
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)