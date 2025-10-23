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
    hsv_ranges = {}  
    for i in defaults: 
        valor_do_usuario = getattr(args, i) 
        if valor_do_usuario is not None:
            hsv_ranges[i] = valor_do_usuario
        else:
            hsv_ranges[i] = defaults[i]
    
    lower_bound = np.array([hsv_ranges['hmin'], hsv_ranges['smin'], hsv_ranges['vmin']])
    upper_bound = np.array([hsv_ranges['hmax'], hsv_ranges['smax'], hsv_ranges['vmax']])
    
    return lower_bound, upper_bound