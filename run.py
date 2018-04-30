from __future__ import print_function
import os
from app import app, server

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    print("**********************************")
    print("   ORDER SERVICE   ")
    print("**********************************")
    server.initialize_logging()
    server.init_db()
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
