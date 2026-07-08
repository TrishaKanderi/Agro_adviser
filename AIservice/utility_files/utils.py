from PIL import Image
import numpy as np
import tensorflow as tf
import cv2
import io


def preprocess_image(image_bytes):

    # Read image
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = np.array(img)

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # Green color range
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([90, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours (leaf regions)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:

        # largest contour = likely leaf
        largest_contour = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(largest_contour)

        # crop leaf area
        leaf = img[y:y+h, x:x+w]

    else:
        # fallback if no contour detected
        leaf = img

    # Resize to model size
    leaf = cv2.resize(leaf, (256, 256))

    leaf = leaf.astype("float32")

    leaf = np.expand_dims(leaf, axis=0)

    return tf.keras.applications.mobilenet_v3.preprocess_input(leaf)