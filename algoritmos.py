import cv2
import numpy as np

def get_color_ranges(target, args):
    """
    Define os ranges HSV padrões para verde e azul, 
    permitindo override pelos argumentos da CLI.
    """
    # Valores padrão para VERDE (H [35-85], S [50-255], V [50-255])
    if target == 'green':
        defaults = {'hmin': 35, 'hmax': 85, 'smin': 50, 'smax': 255, 'vmin': 50, 'vmax': 255}
    # Valores padrão para AZUL (H [90-130], S [50-255], V [50-255])
    elif target == 'blue':
        defaults = {'hmin': 90, 'hmax': 130, 'smin': 50, 'smax': 255, 'vmin': 50, 'vmax': 255}
    else:
        # Se não for verde ou azul, usa um range vazio
        defaults = {'hmin': 0, 'hmax': 0, 'smin': 0, 'smax': 0, 'vmin': 0, 'vmax': 0}

    # Sobrepõe os padrões com o que veio da CLI
    hsv_ranges = {}  # Cria um dicionário vazio
    for i in defaults: # Para cada chave em 'defaults'
        valor_do_usuario = getattr(args, i) # Pega o valor que o usuário digitou
        if valor_do_usuario is not None:
            hsv_ranges[i] = valor_do_usuario
        else:
            # Se ele não digitou, usa o valor padrão
            hsv_ranges[i] = defaults[i]
    
    lower_bound = np.array([hsv_ranges['hmin'], hsv_ranges['smin'], hsv_ranges['vmin']])
    upper_bound = np.array([hsv_ranges['hmax'], hsv_ranges['smax'], hsv_ranges['vmax']])
    
    return lower_bound, upper_bound

def segment_hsv(image, args):
    """ Segmenta a imagem usando thresholding de cor HSV. """
    print(f"Iniciando segmentação HSV para '{args.target}'")
    
    # Converte a imagem de BGR para HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Pega os ranges de cor
    lower_bound, upper_bound = get_color_ranges(args.target, args)
    print(f"Ranges HSV: Baixo={lower_bound}, Alto={upper_bound}")

    # Cria a máscara binária 
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    
    return mask

def segment_kmeans(image, args):
    print(f"Iniciando segmentação K-Means com K={args.k} para '{args.target}'...")

    # prepara a imagem para o K-Means
    pixels = image.reshape((-1, 3))
    pixels = np.float32(pixels) # K-Means exige float32

    # parar após 10 iterações ou se a precisão for 1.0)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    
    # roda o K-Means
    compactness, labels, centers = cv2.kmeans(pixels, args.k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # converte os centros de volta para BGR 8-bit
    centers = np.uint8(centers)

    # Vamos encontrar qual centróide é mais próximo da cor BGR pura.
    if args.target == 'green':
        target_bgr_color = np.array([0, 255, 0]) #verde
    elif args.target == 'blue':
        target_bgr_color = np.array([255, 0, 0]) #azul
    else:
        target_bgr_color = np.array([0, 0, 0]) #preto

    # Calcula a distância de cada centróide até a cor alvo
    distances = [np.linalg.norm(center - target_bgr_color) for center in centers]
    
    target_label = np.argmin(distances)
    print(f"Centróides (BGR): {centers.tolist()}")
    print(f"Distâncias para '{args.target}': {distances}")
    print(f"Cluster alvo escolhido: {target_label} (Cor: {centers[target_label]})")

    # cria a máscara
    mask = (labels.reshape(image.shape[:2]) == target_label).astype(np.uint8) * 255

    return mask
