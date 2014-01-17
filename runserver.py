import os
from ricochet import app

def runserver():
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    runserver()
