
from app import *
from controllers.device import *
from controllers.login import login
from controllers.user import *
from controllers.room import *
from controllers.house import *
from controllers.control import controlDevice

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Welcome"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8085, debug='on')