# main.py
from imageDownloader import downloadTransparentImage
from menu import Menu  # Import the Menu class from the new file


def main():
    complexityConstant = 0.004
    from mbro import Mbro

    bro = Mbro()
    # Get the image to download
    validImage = False
    while not validImage:
        print("Please enter the name of a thing to draw.")
        shape = input()
        try:
            image = downloadTransparentImage(shape)
            validImage = True
        except Exception as e:
            print(e)

    menu = Menu()
    validMenuOption = False
    while not validMenuOption:
        print("Please select a menu option for the following.")
        print(
            "Mbro will start drawing after you select one of these options, and close the window."
        )
        menu.printMenu()
        try:
            selectedOption = int(input())
            menu.executeMethod(selectedOption, args=[image, complexityConstant])
            validMenuOption = True
        except Exception as e:
            print(e)

    bro.drawShape(image, complexityConstant)


if __name__ == "__main__":
    while True:
        main()
