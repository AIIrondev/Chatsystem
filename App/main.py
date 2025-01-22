import ui

def main():
    ui.UI()

if __name__ == '__main__':
    try:
        ui.test_api()
        running_posible = True
    except:
        running_posible = False
        print("API not available")
    if running_posible:
        main()