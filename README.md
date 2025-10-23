# Projeto: Mini-Aplicativo de Segmentação de Imagem

Este projeto é um aplicativo de linha de comando (CLI) em Python capaz de carregar e capturar uma imagem e aplicar dois algoritmos simples de segmentação de imagem: Por Cor em HSV e Agrupamento K-Means.

## Instalação

1.  Clone este repositório
2.  Certifique-se de ter o Python 3.9 ou superior.
3.  Abra o um terminal (ex.: Powershell ou CMD).
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

## Explicação Breve dos Métodos
Este projeto implementa duas abordagens de segmentação baseadas em paradigmas distintos:

### 1. Segmentação por Cor (HSV)
    Este método é uma abordagem direta por limiarização (Thresholding).

    A imagem original é convertida do espaço de cor BGR (padrão do OpenCV) para o HSV (Hue, Saturation, Value). O espaço HSV é preferível para segmentação de cores, pois desacopla a informação de cor pura (H - Matiz) da intensidade da cor (S - Saturação) e do brilho (V - Valor).

    Isso confere robustez a variações de iluminação; mesmo sob sombras (baixo V) ou reflexos especulares (baixo S), o componente H (Matiz) tende a permanecer relativamente estável.

    O método, então, aplica um filtro de limiar. Qualquer pixel cujos valores H, S e V estejam contidos dentro do range especificado (seja pelos valores padrão ou pelos parâmetros da CLI, como --hmin, --smax, etc.) é selecionado e compõe a máscara de segmentação final.

### 2. Segmentação por K-Means (Agrupamento)
    Este método é uma abordagem "não-supervisionada" de Agrupamento (Clustering).

    O algoritmo K-Means não possui conhecimento prévio sobre "azul" ou "verde". Sua função é analisar todos os pixels da imagem e agrupá-los automaticamente em K clusters (definidos pelo usuário via flag --k), com base na similaridade de suas cores no espaço BGR.

    O K-Means identifica os K centróides (as "cores médias") que melhor representam a distribuição de cores da imagem.

    O script, então, analisa esses K centróides e calcula qual deles está matematicamente mais próximo da cor-alvo "pura" especificada pelo usuário no --target (ex: qual centróide tem a menor distância Euclidiana até o BGR "azul puro" [255, 0, 0]).

    A máscara final é gerada selecionando todos os pixels que o algoritmo K-Means atribuiu a esse cluster "vencedor".

## Observações sobre a Escolha de Ranges HSV
    A seleção de um range HSV eficaz é um processo iterativo.

    * **Utilize Ferramentas Auxiliares:** É altamente recomendável usar um "Color Picker" (seletor de cores) que opere em HSV (disponível em softwares como GIMP, Photoshop, ou em ferramentas online). Use-o para extrair os valores H, S e V do pixel-alvo em sua imagem de amostra. Isso fornecerá um ponto de partida para o seu range.

   * ** O Componente H (Matiz) é Primário:** O H (0-179 no OpenCV) define a cor. O primeiro passo é estabelecer um range para ele (ex: Verde situa-se aproximadamente entre 40-80, Azul entre 90-130).

    * **Filtrando Ruído com S e V Mínimos:**
        * S (Saturação) define a "pureza" da cor (0 = escala de cinza, 255 = cor pura).

        * V (Valor) define o brilho da cor (0 = preto, 255 = brilho máximo).

    * **Estratégia de Refinamento:** Para eliminar ruídos comuns, como fundos brancos, cinzas ou superexpostos (reflexos), aumente o limiar --smin (Saturação Mínima) (ex: --smin 50). Para eliminar sombras profundas ou pixels pretos, aumente o limiar --vmin (Valor Mínimo) (ex: --vmin 50). Ajustar os valores mínimos de S e V é a forma mais eficaz de isolar a cor-alvo e limpar a máscara de segmentação.

## Limitações Conhecidas

Embora o script seja funcional, ele possui limitações inerentes aos métodos de segmentação simplificados que utiliza.

### 1. Limitações do Método HSV (--method hsv)
Este método é rápido, mas muito sensível às condições de iluminação e aos parâmetros de entrada.

* **Sensibilidade à Iluminação:** Embora o espaço HSV seja mais robusto a variações de iluminação que o RGB, ele não é imune:

    * **Sombras:** Áreas de sombra intensa reduzem drasticamente o componente V (Brilho) de um pixel. Um objeto verde, por exemplo, pode ficar abaixo do limiar vmin (Valor Mínimo) e não ser segmentado.

    * **Reflexos (Luz Estourada):** Luz direta ou reflexos especulares "lavam" a cor, reduzindo o componente S (Saturação) para próximo de zero. Este pixel "superexposto" ficará abaixo do limiar smin (Saturação Mínima) e também falhará na segmentação.

* **Valores Padrão:** Os ranges de cor padrão (default) para green e blue são apenas estimativas básicas. Na prática, quase sempre será necessário ajustar manualmente os limiares (usando as flags --hmin, --hmax, etc.) para adequar a segmentação às imagens específicas.

* **Segmentação Cíclica (Cor Vermelha):** O espaço de cor HSV é cíclico. A cor vermelha, por exemplo, ocupa dois extremos do range (próximo de 0 e próximo de 179). Este script simples não implementa a lógica de "dar a volta" (wrap-around) e, portanto, não consegue segmentar o vermelho corretamente com um único range.

### 2. Limitações do Método K-Means (--method kmeans)
Este método é mais adaptativo, mas é computacionalmente mais lento e menos direto.

* **Desempenho (Lentidão):** O K-Means é um algoritmo computacionalmente "caro". Ele precisa iterar sobre todos os pixels da imagem múltiplas vezes. Isso pode causar atrasos notáveis, especialmente em imagens de alta resolução ou capturas de webcam.

* **Dependência do Parâmetro K:** O sucesso do método depende de uma boa estimativa do número K de clusters (grupos) pelo usuário:

    *Se K for muito baixo (ex: K=2 em uma cena complexa), o algoritmo pode agrupar cores distintas (ex: azul e verde) no mesmo cluster, invalidando a segmentação.
    
    *Se K for muito alto, ele pode dividir cores semelhantes (ex: "verde-claro" e "verde-escuro") em clusters separados, resultando em uma segmentação incompleta.

* **Seleção do Cluster-Alvo:** A lógica para selecionar o cluster correto (comparando a cor média do centróide com uma cor "pura" como [0, 255, 0]) é simplista. Se o "verde" real da imagem for um tom escuro (ex: verde-musgo), ele pode estar matematicamente mais distante do "verde-puro" do que um cluster de "fundo-branco-sujo", levando o script a selecionar o cluster errado.

