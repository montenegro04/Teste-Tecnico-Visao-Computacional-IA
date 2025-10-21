# Projeto: Mini-Aplicativo de Segmentação de Imagem

Este projeto é um aplicativo de linha de comando (CLI) em Python capaz de carregar uma imagem e aplicar dois algoritmos simples de segmentação de imagem: Thresholding em HSV e Agrupamento K-Means.

## Instalação

1.  Clone este repositório (ou baixe o ZIP).
2.  Certifique-se de ter o Python 3.9 ou superior.
3.  (Recomendado) Crie e ative um ambiente virtual:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # (Linux/Mac)
    # ou
    .\.venv\Scripts\activate   # (Windows)
    ```
4.  Instale as dependências necessárias:
    ```bash
    pip install -r requirements.txt
    ```

## Como Rodar

O script principal é o `segment.py`. Use a flag `--input` para definir a imagem, `--method` para o algoritmo e `--target` para a cor.

### Exemplos de Uso

**Segmentação por Cor (HSV)**

```bash
# Usando os ranges padrão para "verde" na imagem planta1.jpg
python segment.py --input samples/planta1.jpg --method hsv --target green

# Usando os ranges padrão para "azul" e salvando os resultados
python segment.py --input samples/placa.png --method hsv --target blue

# Ajustando manualmente os ranges HSV para "azul"
python segment.py --input samples/placa.png --method hsv --target blue --hmin 90 --hmax 130 --smin 100 --smax 255