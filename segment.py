import cv2
import numpy as np
import argparse
import os
import time

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
        # Se não for verde ou azul, usa um range vazio (não segmenta nada)
        defaults = {'hmin': 0, 'hmax': 0, 'smin': 0, 'smax': 0, 'vmin': 0, 'vmax': 0}

    # Sobrepõe os padrões com o que veio da CLI, se veio
    hsv_ranges = {k: getattr(args, k) if getattr(args, k) is not None else defaults[k] 
                  for k in defaults}
    
    lower_bound = np.array([hsv_ranges['hmin'], hsv_ranges['smin'], hsv_ranges['vmin']])
    upper_bound = np.array([hsv_ranges['hmax'], hsv_ranges['smax'], hsv_ranges['vmax']])
    
    return lower_bound, upper_bound

def segment_hsv(image, args):
    """ Segmenta a imagem usando thresholding de cor HSV. """
    print(f"Iniciando segmentação HSV para '{args.target}'...")
    
    # 1. Converte a imagem de BGR (padrão OpenCV) para HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 2. Pega os ranges de cor (padrão ou da CLI)
    lower_bound, upper_bound = get_color_ranges(args.target, args)
    print(f"Ranges HSV: Baixo={lower_bound}, Alto={upper_bound}")

    # 3. Cria a máscara binária (pixels dentro do range ficam brancos)
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    
    return mask

def segment_kmeans(image, args):
    """ Segmenta a imagem usando K-Means. """
    print(f"Iniciando segmentação K-Means com K={args.k} para '{args.target}'...")

    # 1. Prepara a imagem para o K-Means
    # O K-Means espera uma lista de pixels [R,G,B], [R,G,B], ...
    # Então, "achatamos" a imagem (altura * largura, 3 canais)
    pixels = image.reshape((-1, 3))
    pixels = np.float32(pixels) # K-Means exige float32

    # 2. Define os critérios de parada do K-Means
    # (parar após 10 iterações ou se a precisão (epsilon) for 1.0)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    
    # 3. Roda o K-Means
    # K = args.k
    # compacteness = (retorna a soma das distâncias)
    # labels = (array que diz a qual cluster [0, 1, ... K-1] cada pixel pertence)
    # centers = (os centróides, ou seja, a cor BGR média de cada cluster)
    compactness, labels, centers = cv2.kmeans(pixels, args.k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Converte os centros de volta para BGR 8-bit
    centers = np.uint8(centers)

    # 4. Encontra o cluster "alvo" (verde ou azul)
    # Esta é a parte mais "chatinha".
    # Vamos encontrar qual centróide (cor média do cluster) é mais próximo
    # da cor BGR "pura" que queremos.
    if args.target == 'green':
        target_bgr_color = np.array([0, 255, 0]) # BGR para verde
    elif args.target == 'blue':
        target_bgr_color = np.array([255, 0, 0]) # BGR para azul
    else:
        target_bgr_color = np.array([0, 0, 0]) # Padrão (preto)

    # Calcula a distância (distância Euclidiana) de cada centróide até a cor alvo
    distances = [np.linalg.norm(center - target_bgr_color) for center in centers]
    
    # O cluster que queremos é o que tem a menor distância
    target_label = np.argmin(distances)
    print(f"Centróides (BGR): {centers.tolist()}")
    print(f"Distâncias para '{args.target}': {distances}")
    print(f"Cluster alvo escolhido: {target_label} (Cor: {centers[target_label]})")

    # 5. Cria a máscara
    # "Achatamos" os labels e depois redimensionamos para a imagem original
    # Convertemos para uint8 e multiplicamos por 255 (para ficar 0 ou 255)
    mask = (labels.reshape(image.shape[:2]) == target_label).astype(np.uint8) * 255

    return mask

def save_results(image, mask, base_name):
    """ Salva a máscara e o overlay na pasta 'outputs'. """
    # 1. Garante que a pasta 'outputs' exista
    os.makedirs('outputs', exist_ok=True)
    
    # 2. Define os caminhos de saída
    mask_path = os.path.join('outputs', f"{base_name}_mask.png")
    overlay_path = os.path.join('outputs', f"{base_name}_overlay.png")

    # 3. Cria o overlay semi-transparente
    # Pinta a área da máscara de uma cor (ex: verde)
    color_mask = np.zeros_like(image)
    color_mask[mask == 255] = [0, 255, 0] # Pinta de verde, mude se quiser

    # Mistura a imagem original com a máscara colorida
    # 1.0 * imagem original + 0.4 * máscara colorida
    overlay = cv2.addWeighted(image, 1.0, color_mask, 0.4, 0)

    # 4. Salva os arquivos
    try:
        cv2.imwrite(mask_path, mask)
        cv2.imwrite(overlay_path, overlay)
        print(f"Resultados salvos em '{mask_path}' e '{overlay_path}'")
    except Exception as e:
        print(f"Bah, deu erro ao salvar as imagens: {e}")

def main(args):
    start_time = time.time()
    
    # 1. Carrega a imagem
    image = cv2.imread(args.input)
    if image is None:
        print(f"Erro: Não foi possível carregar a imagem em '{args.input}'")
        return

    # 2. Roda o método escolhido
    if args.method == 'hsv':
        mask = segment_hsv(image, args)
    elif args.method == 'kmeans':
        mask = segment_kmeans(image, args)
    else:
        print(f"Erro: Método '{args.method}' desconhecido.")
        return

    # 3. Salva os resultados
    # Pega o nome do arquivo (ex: 'planta1') sem a extensão
    base_name = os.path.splitext(os.path.basename(args.input))[0]
    base_name += f"_{args.method}_{args.target}" # Ex: planta1_hsv_green
    save_results(image, mask, base_name)
    
    # 4. Log no terminal
    end_time = time.time()
    total_pixels = image.shape[0] * image.shape[1]
    segmented_pixels = cv2.countNonZero(mask)
    percent = (segmented_pixels / total_pixels) * 100
    
    print("-" * 30)
    print(f"Tempo de execução: {end_time - start_time:.4f} segundos")
    print(f"Pixels segmentados: {segmented_pixels} de {total_pixels} ({percent:.2f}%)")
    print("-" * 30)


if __name__ == "__main__":
    # --- Configuração do argparse (CLI) ---
    parser = argparse.ArgumentParser(description="Mini-aplicativo de segmentação de imagem (HSV e K-Means)")
    
    # Entrada
    parser.add_argument("--input", type=str, required=True, help="Caminho para a imagem de entrada.")
    
    # Método
    parser.add_argument("--method", type=str, required=True, choices=['hsv', 'kmeans'], help="Método de segmentação a ser usado.")
    
    # Alvo (cor)
    parser.add_argument("--target", type=str, required=True, choices=['green', 'blue'], help="Cor alvo para a segmentação.")
    
    # Argumentos K-Means
    parser.add_argument("--k", type=int, default=3, help="Número de clusters (K) para o K-Means.")
    
    # Argumentos HSV (opcionais, para ajuste fino)
    parser.add_argument("--hmin", type=int, help="Valor MÍNIMO de Hue (Matiz) [0-179]")
    parser.add_argument("--hmax", type=int, help="Valor MÁXIMO de Hue (Matiz) [0-179]")
    parser.add_argument("--smin", type=int, help="Valor MÍNIMO de Saturation (Saturação) [0-255]")
    parser.add_argument("--smax", type=int, help="Valor MÁXIMO de Saturation (Saturação) [0-255]")
    parser.add_argument("--vmin", type=int, help="Valor MÍNIMO de Value (Brilho) [0-255]")
    parser.add_argument("--vmax", type=int, help="Valor MÁXIMO de Value (Brilho) [0-255]")

    args = parser.parse_args()
    
    # Chama a função principal com os argumentos lidos
    main(args)