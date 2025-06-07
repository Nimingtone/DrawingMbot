from duckduckgo_search import DDGS
import requests
import cv2
import numpy as np


def hasValidShape(image):
    # first check the image has loaded
    # then check it isnt a grayscale image. Should be in form (height,width,channels).
    # so if it's less than 3 it doesnt have any channels.
    # then check if it has 4 channels (RGB + Alpha)
    if image is None or len(image.shape) < 3 or image.shape[2] < 4:
        return False

    #extract alpha and check if any transparency
    alphaChannel = image[:, :, 3]
    #Just because it has an alpha channel, doesnt mean the image itself is transparent.
    #it may have the channel but be fully opaque.
    return np.any(alphaChannel < 255)




def downloadTransparentImage(query):
    #make sure we are searching for simple transparent images.
    query = f"cartoon {query} transparent"

    with DDGS() as ddgs:

        results = ddgs.images(query, max_results=100, safesearch='Off', type_image="transparent")

        results = list(results)

        if not results:
            print("No image found.")
            return None

        #keep looping through images until a valid transparent one is found
        for result in results:
            imageUrl = result['image']
            print(imageUrl)


            #download the image data
            try:
                imageData = requests.get(imageUrl, timeout=5).content
            except Exception as e:
                print(e)

            #convert to cv2 image
            imageArray = np.frombuffer(imageData, dtype=np.uint8)
            cv2Image = cv2.imdecode(imageArray, cv2.IMREAD_UNCHANGED)

            if hasValidShape(cv2Image):
                return cv2Image

        print("No valid transparent image could be found.")
        return None