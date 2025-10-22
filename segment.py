import cv2
import argparse
import os
import time

from algoritmos import segment_hsv, segment_kmeans
from results import save_results

def main(args):
    start_time = time.time()
    
    #carrega a imagem
    image = cv2.imread(args.input)
    if image is None:
        print(f"Erro: Não foi possível carregar a imagem em '{args.input}'")
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
    base_name = os.path.splitext(os.path.basename(args.input))[0]
    base_name += f"_{args.method}_{args.target}" 
    save_results(image, mask, base_name)
    
    end_time = time.time()
    total_pixels = image.shape[0] * image.shape[1]
    segmented_pixels = cv2.countNonZero(mask)
    percent = (segmented_pixels / total_pixels) * 100
    
    print("-" * 30)
    print(f"Tempo de execução: {end_time - start_time:.4f} segundos")
    print(f"Pixels segmentados: {segmented_pixels} de {total_pixels} ({percent:.2f}%)")
    print("-" * 30)


if __name__ == "__main__":
    # configuração do CLI
    parser = argparse.ArgumentParser(description="Mini-aplicativo de segmentação de imagem (HSV e K-Means)")
    
    # entrada
    parser.add_argument("--input", type=str, required=True, help="Caminho para a imagem de entrada.")
    
    # método
    parser.add_argument("--method", type=str, required=True, choices=['hsv', 'kmeans'], help="Método de segmentação a ser usado.")
    
    # alvo (cor)
    parser.add_argument("--target", type=str, required=True, choices=['green', 'blue'], help="Cor alvo para a segmentação.")
    
    # argumentos K-Means
    parser.add_argument("--k", type=int, default=3, help="Número de clusters (K) para o K-Means.")
    
    # argumentos HSV 
    parser.add_argument("--hmin", type=int, help="Valor MÍNIMO de Matiz [0-179]")
    parser.add_argument("--hmax", type=int, help="Valor MÁXIMO de Matiz [0-179]")
    parser.add_argument("--smin", type=int, help="Valor MÍNIMO de Saturação [0-255]")
    parser.add_argument("--smax", type=int, help="Valor MÁXIMO de Saturação [0-255]")
    parser.add_argument("--vmin", type=int, help="Valor MÍNIMO de Brilho [0-255]")
    parser.add_argument("--vmax", type=int, help="Valor MÁXIMO de Brilho [0-255]")

    args = parser.parse_args()
    
    # chama a função principal com os argumentos lidos
    main(args)