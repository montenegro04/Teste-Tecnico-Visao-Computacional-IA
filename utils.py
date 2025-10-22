import os
import numpy as np
import cv2

def capturar_webcam():
    print("Abrindo a webcam. Posicione-se!")
    print(">>> Aperte ESPAÇO para capturar a imagem <<<")
    
    cap = cv2.VideoCapture(0) # liga a câmera, '0' é a câmera padrão (default).

    if not cap.isOpened():
        print("Não foi possível abrir a câmera!")
        return None

    frame = None
    while True:
        ret, frame_preview = cap.read() # Lê um "quadro" (frame) da câmera
        if not ret:
            print("Erro ao ler o frame da câmera.")
            break
            
        frame_preview = cv2.flip(frame_preview, 1)  # "Dá um espelho" na imagem (flipa), senão fica ao contrário

        cv2.imshow("Preview - Aperte ESPAÇO para Capturar", frame_preview)  # Mostra a imagem numa janela

        key = cv2.waitKey(1) & 0xFF  # Espera uma tecla ser apertada (o '1' é 1ms de espera)

        if key == 32: # Se a tecla for ESPAÇO (ASCII código 32)
            print("Foto batida!")
            frame = frame_preview  # Guarda o frame capturado
            break
        
        # Se fechar a janela no "X", também sai (mas não captura)
        if cv2.getWindowProperty("Preview - Aperte ESPAÇO para Capturar", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()  # libera a câmera e fecha as janelas
    
    return frame  # devolve a imagem capturada

def save_results(image, mask, base_name):
    """ Salva a máscara e o overlay na pasta 'outputs'. """
    os.makedirs('outputs', exist_ok=True) #garante que a pasta 'outputs' exista
    
    mask_path = os.path.join('outputs', f"{base_name}_mask.png")
    overlay_path = os.path.join('outputs', f"{base_name}_overlay.png")

    color_mask = np.zeros_like(image)
    color_mask[mask == 255] = [0, 255, 0] # pinta de verde

    overlay = cv2.addWeighted(image, 1.0, color_mask, 0.4, 0)

    try:
        cv2.imwrite(mask_path, mask)
        cv2.imwrite(overlay_path, overlay)
        print(f"Resultados salvos em '{mask_path}' e '{overlay_path}'")
    except Exception as e:
        print(f"Erro ao salvar as imagens: {e}")