# Projeto: Mini-Aplicativo de Segmentação de Imagem

Este projeto é um aplicativo de linha de comando (CLI) em Python capaz de carregar e capturar uma imagem e aplicar dois algoritmos simples de segmentação de imagem: Por Cor em HSV e Agrupamento K-Means.

## Instalação

1.  Clone este repositório
2.  Certifique-se de ter o Python 3.9 ou superior.
3.  Certifique-se de ter uma linha de comando, powershell ou SMD.
4.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # (Linux/Mac)
    # ou
    .\.venv\Scripts\activate   # (Windows)
    ```
5.  Instale as dependências necessárias:
    ```bash
    pip install -r requirements.txt
    ```

## Como Rodar

O script principal é o `segment.py`. Use a flag `--input` ou `--webcam` para definir a imagem ou capturar uma foto ao vivo pela câmera, `--method` para o algoritmo e `--target` para a cor. 
No KMEANS usar após o `--method`: `--k` colocando o número de separações de cores que o método deve fazer

### Exemplos de Uso
```bash
# Usando o método HSV com ranges padrão para "verde"e "azul" nas imagens
python segment.py --input samples/PlantasTeste/plantaRoxa.webp --method hsv --target blue
python segment.py --input samples/PlantasTeste/plantaVermelha.jpg --method hsv --target green #unica imagem jpg

#Usando método KMENS nas imagens
python segment.py --input samples/PlantasTeste/girassol.webp --method kmeans --k 4 --target green
python segment.py --input samples/PlantasTeste/plantaAzul.webp --method kmeans --k 4 --target blue

# Ajustando manualmente os ranges HSV para "azul"
python segment.py --input samples/PlantasTeste/plantaRoxa.webp --method hsv --target blue --hmin 90 --hmax 130 --smin 100 --smax 255

#Usando a captura por webcam por qualquer um dos métodos e cores na cor "verde"
python segment.py --webcam --method kmeans --k 4 --target green
python segment.py --webcam --method hsv --target green