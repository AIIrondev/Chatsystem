from app import main
from app import TestAPI

def crazy():
    main().main_loop()

if __name__ == '__main__':
    try:
        api_tester = TestAPI()
        running_posible = True
    except:
        running_posible = False
        print("API not available")
    if running_posible:
        crazy()
