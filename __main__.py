import sys
from app import create_app

if __name__ == "__main__":
    app = create_app(sys.argv[1])
    app.run(host='0.0.0.0', port=9080)
