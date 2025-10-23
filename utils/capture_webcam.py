import os
import numpy as np
import cv2

def capture_webcam():
    print("Abrindo a webcam. Posicione-se!")
    print(">>> Aperte ESPAÇO para capturar a imagem <<<")
    
    cap = cv2.VideoCapture(0) #liga a câmera, '0' é a câmera padrão.

    if not cap.isOpened():
        print("Não foi possível abrir a câmera!")
        return None

    frame = None
    while True:
        ret, frame_preview = cap.read() 
        if not ret:
            print("Erro ao ler o frame da câmera.")
            break
            
        frame_preview = cv2.flip(frame_preview, 1)  # dá um espelho" na imagem (flipa), senão fica ao contrário

        cv2.imshow("Preview - Aperte ESPAÇO para Capturar", frame_preview) 

        key = cv2.waitKey(1) & 0xFF  

        if key == 32: #se a tecla for ESPAÇO (ASCII código 32)
            print("Foto batida!")
            frame = frame_preview  
            break
        
        if cv2.getWindowProperty("Preview - Aperte ESPAÇO para Capturar", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()  
    
    return frame 
