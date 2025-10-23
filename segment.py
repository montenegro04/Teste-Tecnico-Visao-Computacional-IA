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
    
    parser.add_argument("--hmin", type=int, help="Valor MÍNIMO de Matiz [0-179]")
    parser.add_argument("--hmax", type=int, help="Valor MÁXIMO de Matiz [0-179]")
    parser.add_argument("--smin", type=int, help="Valor MÍNIMO de Saturação [0-255]")
    parser.add_argument("--smax", type=int, help="Valor MÁXIMO de Saturação [0-255]")
    parser.add_argument("--vmin", type=int, help="Valor MÍNIMO de Brilho [0-255]")
    parser.add_argument("--vmax", type=int, help="Valor MÁXIMO de Brilho [0-255]")

    args = parser.parse_args()

    if args.method == 'hsv':
        if args.hmin is not None and (args.hmin < 0 or args.hmin > 179):
            parser.error("--hmin deve estar entre 0 e 179")
        if args.hmax is not None and (args.hmax < 0 or args.hmax > 179):
            parser.error(" --hmax deve estar entre 0 e 179.")
       
        if args.smin is not None and (args.smin < 0 or args.smin > 255):
            parser.error("--smin deve estar entre 0 e 255")
        if args.smax is not None and (args.smax < 0 or args.smax > 255):
            parser.error("--smax deve estar entre 0 e 255.")

        if args.vmin is not None and (args.vmin < 0 or args.vmin > 255):
            parser.error("--vmin deve estar entre 0 e 255.")
        if args.vmax is not None and (args.vmax < 0 or args.vmax > 255):
            parser.error("--vmax deve estar entre 0 e 255.")
    
        if args.hmin is not None and args.hmax is not None:
                if args.hmin > args.hmax:
                    parser.error("--hmin não pode ser MAIOR que o --hmax.")
            
        if args.smin is not None and args.smax is not None:
                if args.smin > args.smax:
                    parser.error(" --smin não pode ser MAIOR que o --smax.")

        if args.vmin is not None and args.vmax is not None:
                if args.vmin > args.vmax:
                    parser.error("--vmin não pode ser MAIOR que o --vmax.")

    if args.method == 'kmeans':
        if args.k <= 0:
            parser.error("--k tem que ser no mínimo 1!")

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