import matplotlib.pyplot as plt
from outline import extractVectorOutline

def plotImages(image, complexityConstant):
    # Extract the vector outline
    vector_outline, mask, contour = extractVectorOutline(
        image,
        complexityConstant=complexityConstant,  # Lower value keeps more detail
    )

    #create a figure for visualization
    plt.figure(figsize=(12, 10))

    #display the original image
    plt.subplot(2, 2, 1)
    plt.imshow(image)
    plt.title("Original Image")
    plt.axis("off")

    #display the transparency mask
    plt.subplot(2, 2, 2)
    plt.imshow(mask, cmap="gray")
    plt.title("Transparency Mask")
    plt.axis("off")

    #display the vector outline with a light gray background
    plt.subplot(2, 2, 4)
    plt.gca().set_facecolor("lightgray")
    plt.axis("equal")
    plt.title("Vector Outline")

    #extract X, Y coordinates from the vector outline
    xCoords, yCoords = zip(*vector_outline)

    #draw green outline and mark red vertices
    plt.plot(
        xCoords + (xCoords[0],),  #close the shape by connecting last point to first
        yCoords + (yCoords[0],),
        color="green",
        linewidth=2,
    )
    plt.scatter(xCoords, yCoords, color="red", s=20)

    #show the final plots
    plt.show()