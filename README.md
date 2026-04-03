

---

# Problema do Carteiro Chinês (PCC) - Trabalho Prático 3

Este projeto implementa uma solução para o **Problema do Carteiro Chinês** em dígrafos ponderados. O objetivo é encontrar o circuito de menor custo que percorra todas as arestas de um grafo dirigido pelo menos uma vez.

## 📋 Descrição da Eulerização

Para que um dígrafo admita um circuito euleriano, ele deve estar **balanceado** (o grau de entrada de cada vértice deve ser igual ao seu grau de saída) e ser fortemente conexo.

A eulerização deste trabalho foi realizada manualmente através da análise do grafo original (`entrada_original.txt`). Foram identificados os vértices desbalanceados e adicionadas arestas repetidas para equilibrar os graus:

* **Vértices Originais**: O grafo original possui 6 vértices e 11 arestas.
* **Arestas Adicionadas**: Para balancear o grafo, foram replicadas arestas nos seguintes caminhos (marcadas com `*` no arquivo de entrada):
    * `5 -> 2` (peso 22)
    * `4 -> 0` (peso 12) - adicionada duas vezes
    * `3 -> 4` (peso 5)
    * `2 -> 3` (peso 20)
    * `0 -> 1` (peso 10)
* **Resultado**: O grafo final (`entrada_eulerizada.txt`) possui 17 arestas, resultando em um circuito total de custo **276**.

## 🚀 Instruções de Execução

O projeto foi desenvolvido em **Python** e utiliza uma estrutura baseada na biblioteca `algs4`.

### Pré-requisitos
* Python 3.11 ou superior.
* Jupyter Notebook (opcional, para rodar o `main.ipynb`).

### Como executar
1.  Certifique-se de que os arquivos de dados estão na pasta `pcc/dados/`.
2.  Navegue até a pasta `pcc/src/`.
3.  Execute o script principal (ou abra o notebook):
    ```bash
    python main.py
    ```
    *(Nota: Se estiver usando o notebook `main.ipynb`, execute todas as células para ver a saída formatada)*.

## 🛠 Estrutura do Código
* `bag.py`: Implementação de uma coleção Bag para a lista de adjacência.
* `digraph.py`: Estrutura de dados para o dígrafo ponderado.
* `directed_edge.py`: Representação de uma aresta dirigida com peso.
* `DirectedEulerianCycle.py`: Implementação do **Algoritmo de Hierholzer** para encontrar o circuito euleriano.
* `main.ipynb`: Ponto de entrada que carrega os dados e exibe os resultados.

## 🎥 Vídeo Explicativo
O vídeo com a explicação técnica e demonstração da execução pode ser acessado no link abaixo:
* [https://www.youtube.com/]

---

### Resultados Obtidos (Exemplo de Saída)
Ao processar o arquivo eulerizado, o programa gera a seguinte saída:
* **Graus**: Todos os vértices apresentam `in_degree == out_degree`.
* **Circuito Encontrado**: `a → b → d → e → a → b → e → a → c → e → f → c → d → f → c → d → e → a`.
* **Custo Total**: 276.