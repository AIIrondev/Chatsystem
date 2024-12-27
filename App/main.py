from ui import UI
from database import Database
from database import User

def setup():
    Database()
    User()


if __name__ == '__main__':
    setup()
    UI().register()