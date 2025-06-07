# menu.py
from TurtleDrawer import drawShapeTurtle
from ImagePlotter import plotImages

class Menu:
    def __init__(self):
        self.__options = {
            1: {"description": "Draw shape in turtle",
                "method": drawShapeTurtle},
            2: {"description": "View image plot.",
                 "method": plotImages}
        }

    def getMenuOption(self, selectedOption):
        if selectedOption not in self.__options:
            raise ValueError("That is not a valid option!")
        return self.__options[selectedOption]["method"]

    def printMenu(self):
        for index, menuOption  in self.__options.items():
            print(f"{index}> {menuOption["description"]}")

    def executeMethod(self,option,args):
        method = self.getMenuOption(option)
        method(*args)