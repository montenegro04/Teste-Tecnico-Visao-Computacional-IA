# Projeto: Mini-Aplicativo de Segmentação de Imagem

Este projeto é um aplicativo de linha de comando (CLI) em Python capaz de carregar e capturar uma imagem e aplicar dois algoritmos simples de segmentação de imagem: Por Cor em HSV e Agrupamento K-Means.

## Instalação

1.  Clone este repositório
2.  Certifique-se de ter o Python 3.9 ou superior.
3.  Abra o um terminal (ex.: Powershel ou CMD).
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
No KMEANS usar `--k` colocando o número de separações de cores que o método deve fazer.

### Exemplos de Uso
```bash
# Usando o método HSV com ranges padrão para "verde"e "azul" nas imagens
python segment.py --input samples/PlantsTest/plantaRoxa.webp --method hsv --target blue
python segment.py --input samples/PlantsTest/plantaVermelha.jpg --method hsv --target green #unica imagem jpg

#Usando método KMENS nas imagens
python segment.py --input samples/PlantsTest/girassol.webp --method kmeans --k 4 --target green
python segment.py --input samples/PlantsTest/plantaAzul.webp --method kmeans --k 4 --target blue

# Ajustando manualmente os ranges HSV para "azul"
python segment.py --input samples/PlantsTest/plantaRoxa.webp --method hsv --target blue --hmin 90 --hmax 130 --smin 100 --smax 255

#Usando a captura por webcam por qualquer um dos métodos e cores
python segment.py --webcam --method kmeans --k 4 --target green
python segment.py --webcam --method hsv --target blue
```
## Limitações Conhecidas

Embora o script seja funcional, ele possui limitações inerentes aos métodos de segmentação simplificados que utiliza.

### 1. Limitações do Método HSV (--method hsv)
Este método é rápido, mas muito sensível às condições de iluminação e aos parâmetros de entrada.

* **Sensibilidade à Iluminação:** Embora o espaço HSV seja mais robusto a variações de iluminação que o RGB, ele não é imune:

    * **Sombras:** Áreas de sombra intensa reduzem drasticamente o componente V (Brilho) de um pixel. Um objeto verde, por exemplo, pode ficar abaixo do limiar vmin (Valor Mínimo) e não ser segmentado.

    * **Reflexos (Luz Estourada):** Luz direta ou reflexos especulares "lavam" a cor, reduzindo o componente S (Saturação) para próximo de zero. Este pixel "superexposto" ficará abaixo do limiar smin (Saturação Mínima) e também falhará na segmentação.

**Valores Padrão:** Os ranges de cor padrão (default) para green e blue são apenas estimativas básicas. Na prática, quase sempre será necessário ajustar manualmente os limiares (usando as flags --hmin, --hmax, etc.) para adequar a segmentação às imagens específicas.

**Segmentação Cíclica (Cor Vermelha):** O espaço de cor HSV é cíclico. A cor vermelha, por exemplo, ocupa dois extremos do range (próximo de 0 e próximo de 179). Este script simples não implementa a lógica de "dar a volta" (wrap-around) e, portanto, não consegue segmentar o vermelho corretamente com um único range.

### 2. Limitações do Método K-Means (--method kmeans)
Este método é mais adaptativo, mas é computacionalmente mais lento e menos direto.

**Desempenho (Lentidão):** O K-Means é um algoritmo computacionalmente "caro". Ele precisa iterar sobre todos os pixels da imagem múltiplas vezes. Isso pode causar atrasos notáveis, especialmente em imagens de alta resolução ou capturas de webcam.

**Dependência do Parâmetro K:** O sucesso do método depende de uma boa estimativa do número K de clusters (grupos) pelo usuário:

    *Se K for muito baixo (ex: K=2 em uma cena complexa), o algoritmo pode agrupar cores distintas (ex: azul e verde) no mesmo cluster, invalidando a segmentação.*
    
    *Se K for muito alto, ele pode dividir cores semelhantes (ex: "verde-claro" e "verde-escuro") em clusters separados, resultando em uma segmentação incompleta.*

**Seleção do Cluster-Alvo:** A lógica para selecionar o cluster correto (comparando a cor média do centróide com uma cor "pura" como [0, 255, 0]) é simplista. Se o "verde" real da imagem for um tom escuro (ex: verde-musgo), ele pode estar matematicamente mais distante do "verde-puro" do que um cluster de "fundo-branco-sujo", levando o script a selecionar o cluster errado.

