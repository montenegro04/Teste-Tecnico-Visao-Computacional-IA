import cv2
import numpy as np
import os

def save_results(image, mask, base_name, target_color):
    """ Salva a máscara e o overlay na pasta 'outputs'. """
    os.makedirs('outputs', exist_ok=True)
    
    mask_path = os.path.join('outputs', f"{base_name}_mask.png")
    overlay_path = os.path.join('outputs', f"{base_name}_overlay.png")

    if target_color == 'green':
        paint_color_bgr = [0, 255, 0] # Verde
    elif target_color == 'blue':
        paint_color_bgr = [255, 0, 0] # azul
    else:
        paint_color_bgr = [0, 0, 255]

    color_mask = np.zeros_like(image)
    color_mask[mask == 255] = paint_color_bgr

    overlay = cv2.addWeighted(image, 1.0, color_mask, 0.4, 0)

    try:
        cv2.imwrite(mask_path, mask)
        cv2.imwrite(overlay_path, overlay)
        print(f"Resultados salvos em '{mask_path}' e '{overlay_path}'")
    except Exception as e:
        print(f"Erro ao salvar as imagens: {e}")