import cv2
import argparse
import os
import time

from algoritmos import segment_hsv, segment_kmeans
from utils import save_results, capturar_webcam

def configurar_argumentos_cli():
    parser = argparse.ArgumentParser(description="Mini-aplicativo de segmentação de imagem (HSV e K-Means)")
    
    grupo_entrada = parser.add_mutually_exclusive_group(required=True)
    grupo_entrada.add_argument("--input", type=str, help="Caminho para a imagem de entrada.")
    grupo_entrada.add_argument("--webcam", action='store_true', help="Captura a imagem da webcam.")    
    # action=store_true faz o args.webcam virar True se a flag for usada.

    parser.add_argument("--method", type=str, required=True, choices=['hsv', 'kmeans'], help="Método de segmentação.")
    parser.add_argument("--target", type=str, required=True, choices=['green', 'blue'], help="Cor alvo para a segmentação.")
    parser.add_argument("--k", type=int, default=3, help="Número de clusters (K) para o K-Means.")
    
    parser.add_argument("--hmin", type=int, help="Valor MÍNIMO de Hue [0-179]")
    parser.add_argument("--hmax", type=int, help="Valor MÁXIMO de Hue [0-179]")
    parser.add_argument("--smin", type=int, help="Valor MÍNIMO de Saturation [0-255]")
    parser.add_argument("--smax", type=int, help="Valor MÁXIMO de Saturation [0-255]")
    parser.add_argument("--vmin", type=int, help="Valor MÍNIMO de Value [0-255]")
    parser.add_argument("--vmax", type=int, help="Valor MÁXIMO de Value [0-255]")

    args = parser.parse_args()
    return args

def main(args):
    start_time = time.time() #coleta o tempo real
    
    if args.input:
        image = cv2.imread(args.input)
    elif args.webcam:
        image = capturar_webcam()
    
    if image is None:
        if args.input:
            print(f"Erro: Não foi possível carregar a imagem em '{args.input}'")
        else:
            print("Captura da webcam cancelada ou falhou.")
        return

    #roda o método escolhido
    if args.method == 'hsv':
        mask = segment_hsv(image, args)
    elif args.method == 'kmeans':
        mask = segment_kmeans(image, args)
    else:
        print(f"Erro: Método '{args.method}' desconhecido.")
        return

    #salva os resultados
    if args.input:
        base_name = os.path.splitext(os.path.basename(args.input))[0]
    else:
        base_name = f"webcam_captura_{int(time.time())}"

    base_name += f"_{args.method}_{args.target}"
    save_results(image, mask, base_name)
    
    end_time = time.time() #encerra o tempo
    total_pixels = image.shape[0] * image.shape[1]
    segmented_pixels = cv2.countNonZero(mask) #diz quantos pixels ñ são zeros na mascara
    percent = (segmented_pixels / total_pixels) * 100
    
    print("-" * 30)
    print(f"Tempo de execução: {end_time - start_time:.4f} segundos")
    print(f"Pixels segmentados: {segmented_pixels} de {total_pixels} ({percent:.2f}%)")
    print("-" * 30)


if __name__ == "__main__":
    args = configurar_argumentos_cli() 
    main(args)