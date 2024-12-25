from ui import UI
from database import Database_Messages

def setup():
    Database_Messages()


if __name__ == '__main__':
    setup()
    UI().run()