import time
import cyberpi
import math
from outline import extractVectorOutline
from instructionQueue import Instructions, Instruction
from threading import Thread


class Mbro:
    def __init__(self):
        # time.sleep(5)
        print("Cyber-pi has started...")
        self.__WiFiConnected = self.connectToWifi()
        self.__motorSpeed = 150
        self.__imageScaleDivisor = 64
        self.__wheelRadius = 3
        self.__instructions = Instructions()
        self.__paperColour = (255, 255, 255)
        self.__isDrawing = False
        self.__RGBThreshold = 50
        self.__ultrasonicStoppingDistanceRange = {"min": 5, "max": 10}

    def setDrawing(self, val):
        self.__isDrawing = val

    def isDrawing(self):
        return self.__isDrawing

    def connectToWifi(self, timeout=10):
        cyberpi.wifi.connect("SwanseaUni-Play", "time-to-play")
        start = time.time()
        while time.time() - start < timeout:
            wifiConnected = cyberpi.wifi.is_connect()
            if wifiConnected:
                print("Succesffully connected to WiFi...")
                return True
            time.sleep(0.5)
        print("Could not connect to WiFi...")
        return False

    def turn(self, degrees):
        cyberpi.mbot2.turn(degrees, self.__motorSpeed)

    def turn_left(self, degrees):
        cyberpi.reset_yaw()
        cyberpi.mbot2.turn_left(10)
        while abs(cyberpi.get_yaw()) < abs(degrees):
            time.sleep(0.0001)
            # print(cyberpi.get_yaw())
        cyberpi.mbot2.EM_stop()
        print(cyberpi.get_yaw())

    def turn_right(self, degrees):
        cyberpi.reset_yaw()
        cyberpi.mbot2.turn_right(10)
        while abs(cyberpi.get_yaw()) < (degrees * 1):
            time.sleep(0.00001)
            # print(abs(cyberpi.get_yaw()))
        cyberpi.mbot2.EM_stop()
        print(cyberpi.get_yaw())

    # def turn(self,degrees):
    #     if degrees < 0:
    #         self.turn_left(abs(degrees))
    #     else:
    #         self.turn_right(abs(degrees))

    def getQuadRGB(self):
        return (
            cyberpi.quad_rgb_sensor.get_red(1, 1),
            cyberpi.quad_rgb_sensor.get_green(1, 1),
            cyberpi.quad_rgb_sensor.get_blue(1, 1),
        )

    def setPaperColour(self):
        self.__paperColour = self.getQuadRGB()

    # experimenting with different ways to detect colour differences
    def isOnPaper(self):
        rgbvalues = self.getQuadRGB()
        for i in range(len(rgbvalues)):
            if abs((rgbvalues[i]) - self.__paperColour[i]) > self.__RGBThreshold:
                return False
        return True

    def isOnPaper(self):
        rgbvalues = self.getQuadRGB()
        if abs(sum(rgbvalues) - sum(self.__paperColour)) >= self.__RGBThreshold:
            return False
        return True

    # best approach for detecting colour differences using euclidian distance
    def isOnPaper(self):
        r2, g2, b2 = self.getQuadRGB()
        r1, g1, b1 = self.__paperColour

        colorDifference = math.sqrt((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2)

        if abs(colorDifference) >= self.__RGBThreshold:
            return False
        return True

    def getUltrasonicDistance(self):
        return cyberpi.ultrasonic2.get(1)

    def getLightSensor(self):
        return cyberpi.light_sensor.get()

    def forward(self, distance, speed):
        cyberpi.mbot2.straight(distance, speed)

    def createInstructionSet(self, image, complexityConstant):
        vector_outline, mask, contour = extractVectorOutline(
            image,
            complexityConstant=complexityConstant,  # Lower value keeps more detail
        )

        # add the first point to the very end so it does full loop
        vector_outline.append(vector_outline[0])
        x1, y1 = vector_outline[0]
        currentangle = (
            0  # this is the current angle relative to the robot's starting position
        )

        for v in range(1, len(vector_outline)):
            x2, y2 = vector_outline[v]
            # using pythagorus to get the distance
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            # get the angle between the 2 points
            bearing = math.degrees(math.atan2(y2 - y1, x2 - x1))

            # normalise the angle so mbot doesnt start trickshotting
            relativeAngle = (bearing - currentangle + 180) % 360 - 180

            self.__instructions.addInstruction(
                instruction=Instruction(type="turn", value=-relativeAngle)
            )

            self.__instructions.addInstruction(
                instruction=Instruction(
                    type="forward", value=(distance / self.__imageScaleDivisor)
                )
            )

            # update the current coords
            x1, y1 = x2, y2
            currentangle = bearing

    def __sensorChecking(self):
        while self.__isDrawing:
            ultrasonicValue = self.getUltrasonicDistance()
            print(f"ultrasonicValue: {ultrasonicValue}")
            if (
                ultrasonicValue < self.__ultrasonicStoppingDistanceRange["max"]
                and ultrasonicValue > self.__ultrasonicStoppingDistanceRange["min"]
            ):
                self.__isDrawing = False
                self.__instructions.abortQueue()
                cyberpi.mbot2.EM_stop()
                print("Drawing interupted. Obstacle")
                return
            if not self.isOnPaper():
                self.__isDrawing = False
                self.__instructions.abortQueue()
                cyberpi.mbot2.EM_stop()
                print("Drawing interuppted. off paper")
                return
            time.sleep(0.05)

    def drawShape(self, image, complexityConstant):
        self.setPaperColour()
        self.createInstructionSet(image, complexityConstant)
        self.__isDrawing = True
        Thread(target=self.__sensorChecking, args=[]).start()
        while self.__isDrawing:
            instruction = self.__instructions.executeInstruction()
            print(f"paper colour {self.__paperColour}")
            print(f"current RGB val {self.getQuadRGB()}")

            # guard clauses to stop drawing
            if instruction is None or not self.__instructions.hasInstructions():
                print("Finished drawing")
                self.__isDrawing = False
                return

            if instruction.getInstructionType() == "turn":
                self.turn(instruction.getInstructionValue() - 0.5)
            elif instruction.getInstructionType() == "forward":
                self.forward(instruction.getInstructionValue(), self.__motorSpeed)
