class Instructions:
    def __init__(self):
        self.__queue = []

    def addInstruction(self,instruction):
        self.__queue.append(instruction)

    def executeInstruction(self):
        if not self.hasInstructions():
            return None
        return self.__queue.pop(0)

    def hasInstructions(self):
        if len(self.__queue) == 0:
            return False 
        return True
    
    def abortQueue(self):
        self.__queue = []


class Instruction:
    def __init__(self,type,value):
        self.__type = type
        self.__value = value

    def getInstructionType(self):
        return  self.__type

    def getInstructionValue(self):
        return self.__value
