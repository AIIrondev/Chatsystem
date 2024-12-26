from ui import UI
from database import Database

def setup():
    Database()


if __name__ == '__main__':
    setup()
    UI().run()