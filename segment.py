import cv2
import argparse
import time
import os

from segmentation.hsv_segmenter import segment_hsv
from segmentation.kmeans_segmenter import segment_kmeans
from utils.save_results import save_results
from utils.capture_webcam import capture_webcam

def config_argument_cli():
    parser = argparse.ArgumentParser(description="Mini-aplicativo de segmentação de imagem (HSV e K-Means)")
    
    grup_input = parser.add_mutually_exclusive_group(required=True)
    grup_input.add_argument("--input", type=str, help="Caminho para a imagem de entrada.")
    grup_input.add_argument("--webcam", action='store_true', help="Captura a imagem da webcam.")    

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

    if args.method == 'hsv':
        if args.hmin is not None and (args.hmin < 0 or args.hmin > 179):
            parser.error("--hmin deve estar entre 0 e 179")
        if args.smin is not None and (args.smin < 0 or args.smin > 255):
            parser.error("--smin deve estar entre 0 e 255")
    return args

def main(args):
    start_time = time.time() 
    
    if args.input:
        image = cv2.imread(args.input)
    elif args.webcam:
        image = capture_webcam()
    
    if image is None:
        if args.input:
            print(f"Erro: Não foi possível carregar a imagem em '{args.input}'")
        else:
            print("Captura da webcam cancelada ou falhou.")
        return

    if args.method == 'hsv':
        mask = segment_hsv(image, args)
    elif args.method == 'kmeans':
        mask = segment_kmeans(image, args)
    else:
        print(f"Erro: Método '{args.method}' desconhecido.")
        return

    if args.input:
        base_name = os.path.splitext(os.path.basename(args.input))[0]
    else:
        base_name = f"webcam_captura_{int(time.time())}"

    base_name += f"_{args.method}_{args.target}"
    save_results(image, mask, base_name, args.target)
    
    end_time = time.time()
    total_pixels = image.shape[0] * image.shape[1]
    segmented_pixels = cv2.countNonZero(mask)    #diz quantos pixels ñ são zeros na mascara
    percent = (segmented_pixels / total_pixels) * 100
    
    print("-" * 30)
    print(f"Tempo de execução: {end_time - start_time:.4f} segundos")
    print(f"Pixels segmentados: {segmented_pixels} de {total_pixels} ({percent:.2f}%)")
    print("-" * 30)


if __name__ == "__main__":
    args = config_argument_cli() 
    main(args)