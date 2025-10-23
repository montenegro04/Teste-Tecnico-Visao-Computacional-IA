import cv2
import numpy as np
from segmentation.color_ranges import get_color_ranges

def segment_hsv(image, args):
    """ Segmenta a imagem usando thresholding de cor HSV. """
    print(f"Iniciando segmentação HSV para '{args.target}'")
    
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower_bound, upper_bound = get_color_ranges(args.target, args)    # Pega os ranges de cor
    print(f"Ranges HSV: Baixo={lower_bound}, Alto={upper_bound}")

    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    return mask