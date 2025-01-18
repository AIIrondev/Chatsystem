from ui import UI
from database import Database
from database import User
from database import Chatroom

def setup():
    Chatroom()
    Database()
    User()


if __name__ == '__main__':
    setup()
    try:
        UI().register()
    except:
        UI.close()