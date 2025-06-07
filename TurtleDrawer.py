import turtle
import math
from outline import extractVectorOutline


def drawShapeTurtle(image, complexityConstant):
    # Extract the vector outline
    vector_outline, mask, contour = extractVectorOutline(
        image,
        complexityConstant=complexityConstant,  # lower value keeps more detail
    )

    # add the first point to the very end so it does full loop
    vector_outline.append(vector_outline[0])

    t = turtle.Turtle()
    t.speed(15)
    x1, y1 = vector_outline[0]
    currentangle = (
        0  # this is the current angle relative to the robot's starting position
    )

    t.pendown()

    for v in range(1, len(vector_outline)):
        x2, y2 = vector_outline[v]
        # using pythagorus to get the distance
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # get the angle between the 2 points
        bearing = math.degrees(math.atan2(y2 - y1, x2 - x1))

        # normalise the angle so mbot doesnt start trickshotting
        relativeAngle = (bearing - currentangle + 180) % 360 - 180

        # now turn and draw
        t.left(relativeAngle) if relativeAngle > 1 else t.right(-relativeAngle)

        t.forward(distance / 2)

        # update the current coords
        x1, y1 = x2, y2
        currentangle = bearing
    turtle.mainloop()

