import sys

from website import create_app
from flask_cors import CORS

if __name__ == "__main__":
    app = create_app()
    CORS(app, support_credentials=True)
    app.run(host='0.0.0.0', port=int(sys.argv[1]))