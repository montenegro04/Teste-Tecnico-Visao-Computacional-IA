import os
import numpy as np
import cv2

def save_results(image, mask, base_name):
    """ Salva a máscara e o overlay na pasta 'outputs'. """
    #garante que a pasta 'outputs' exista
    os.makedirs('outputs', exist_ok=True)
    
    mask_path = os.path.join('outputs', f"{base_name}_mask.png")
    overlay_path = os.path.join('outputs', f"{base_name}_overlay.png")

    color_mask = np.zeros_like(image)
    color_mask[mask == 255] = [0, 255, 0] # Pinta de verde, mude se quiser

    overlay = cv2.addWeighted(image, 1.0, color_mask, 0.4, 0)

    try:
        cv2.imwrite(mask_path, mask)
        cv2.imwrite(overlay_path, overlay)
        print(f"Resultados salvos em '{mask_path}' e '{overlay_path}'")
    except Exception as e:
        print(f"Erro ao salvar as imagens: {e}")