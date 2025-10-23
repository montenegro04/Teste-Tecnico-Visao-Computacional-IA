import cv2
import numpy as np

def segment_kmeans(image, args):
    print(f"Iniciando segmentação K-Means com K={args.k} para '{args.target}'...")

    pixels = image.reshape((-1, 3))
    pixels = np.float32(pixels) # K-Means exige float32

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    
    compactness, labels, centers = cv2.kmeans(pixels, args.k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    centers = np.uint8(centers)  # converte os centros de volta para BGR 8-bit

    if args.target == 'green':
        target_bgr_color = np.array([0, 255, 0]) #verde
    elif args.target == 'blue':
        target_bgr_color = np.array([255, 0, 0]) #azul
    else:
        target_bgr_color = np.array([0, 0, 0]) #preto

    distances = [np.linalg.norm(center - target_bgr_color) for center in centers]
    
    target_label = np.argmin(distances)
    print(f"Centróides (BGR): {centers.tolist()}")
    print(f"Distâncias para '{args.target}': {distances}")
    print(f"Cluster alvo escolhido: {target_label} (Cor: {centers[target_label]})")

    mask = (labels.reshape(image.shape[:2]) == target_label).astype(np.uint8) * 255
    return mask