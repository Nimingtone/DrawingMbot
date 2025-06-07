import cv2

binSize = 768


def extractVectorOutline(image, complexityConstant=0.01, plot=True):
    # first check the image has loaded
    # then check it isnt a grayscale image. Should be in form (height,width,channels).
    # so if it's less than 3 it doesnt have any channels.
    # then check if it has 4 channels (RGB + Alpha)
    if image is None or len(image.shape) < 3 or image.shape[2] < 4:
        raise ValueError(
            "Error: Image must have an alpha channel (transparent background)."
        )

    # extract the alpha channel (transparency)
    # https://stackoverflow.com/questions/32290096/python-opencv-add-alpha-channel-to-rgb-image
    alphaChannel = image[:, :, 3]

    # convert transparency into a binary mask (255 = visible, 0 = transparent)
    # https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
    # https://pyimagesearch.com/2021/04/28/opencv-thresholding-cv2-threshold/
    ret, mask = cv2.threshold(alphaChannel, 1, 255, cv2.THRESH_BINARY)

    # find contours (external shape only)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # if no contours were found, the image is likely empty or fully transparent
    if len(contours) == 0:
        raise ValueError("Error: No valid shape detected in the image.")

    # get the largest contour (assuming it's the main shape)
    largestContour = max(contours, key=cv2.contourArea)

    # compute epsilon (Higher number means more simple)
    # https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
    # https://pyimagesearch.com/2021/10/06/opencv-contour-approximation/
    countourLength = cv2.arcLength(largestContour, True)
    epsilon = complexityConstant * countourLength

    # simplify the contour
    simplifiedContour = cv2.approxPolyDP(largestContour, epsilon, True)

    # convert contour points from OpenCV format to a list of tuples
    vectorPath = []
    for point in simplifiedContour:
        x, y = point[0]  # extract x and y
        vectorPath.append(
            (int(x), -int(y))
        )  # for some reason coords are upside down. Dont think cv2 uses cartesian coordinate system

    print(vectorPath)

    # bin the vectors to a fixed size while preserving aspect ratio
    imageHeight = max(v[0] for v in vectorPath) - min(v[0] for v in vectorPath)
    imageWidth = max(v[1] for v in vectorPath) - min(v[1] for v in vectorPath)
    scaleFactor = float(binSize / max(imageWidth, imageHeight))

    scaledPath = [(x * scaleFactor, y * scaleFactor) for x, y in vectorPath]

    if plot:
        return scaledPath, mask, simplifiedContour
    return scaledPath
