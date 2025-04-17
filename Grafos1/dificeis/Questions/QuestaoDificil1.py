from collections import deque
import sys

def bfs_caminho_minimo(n, grafo, s):
    """
    Executa uma BFS a partir do vértice s em um grafo não ponderado e retorna
    a lista de distâncias mínimas de s a todos os vértices.
    Cada aresta é considerada de peso 6 (conforme o problema original).
    """
    # Inicializa todas as distâncias como -1 (não alcançado)
    distancias = [-1] * (n + 1)
    # Distância de s para si mesmo é zero
    distancias[s] = 0

    # Cria uma fila e enfileira o vértice inicial
    fila = deque([s])

    # Executa BFS
    while fila:
        atual = fila.popleft()            # Desenfileira o próximo vértice a explorar
        for vizinho in grafo[atual]:      # Para cada vizinho de 'atual'
            if distancias[vizinho] == -1: # Se ainda não foi visitado
                # Marca a distância do vizinho como distância de 'atual' + 6
                distancias[vizinho] = distancias[atual] + 6
                fila.append(vizinho)      # Enfileira o vizinho para continuar a BFS

    return distancias

def resolver():
    """
    Lê múltiplos casos de teste do stdin no formato:
      t
      n m
      u1 v1
      u2 v2
      ...
      um vm
      s
      (próximo caso)
    Para cada caso, constrói o grafo, executa bfs_caminho_minimo e imprime
    as distâncias de s a todos os outros vértices (exceto s).
    """
    dados = sys.stdin.read().split()
    t = int(dados[0])    # número de casos de teste
    indice = 1           # índice de leitura em 'dados'
    resultados = []      # lista para armazenar resultados de cada caso

    for _ in range(t):
        # Lê n (vértices) e m (arestas)
        n = int(dados[indice])
        m = int(dados[indice + 1])
        indice += 2

        # Inicializa lista de adjacência para grafo com vértices de 1 a n
        grafo = [[] for _ in range(n + 1)]

        # Lê todas as arestas
        for _ in range(m):
            u = int(dados[indice])
            v = int(dados[indice + 1])
            indice += 2
            # Como o grafo é não direcionado, adiciona em ambas as direções
            grafo[u].append(v)
            grafo[v].append(u)

        # Lê o vértice inicial s
        s = int(dados[indice])
        indice += 1

        # Executa BFS para obter distâncias mínimas a partir de s
        distancias = bfs_caminho_minimo(n, grafo, s)

        # Prepara a linha de saída, ignorando o próprio s
        res = []
        for i in range(1, n + 1):
            if i == s:
                continue
            res.append(str(distancias[i]))

        resultados.append(" ".join(res))

    # Imprime todos os resultados, um caso por linha
    sys.stdout.write("\n".join(resultados))

if __name__ == '__main__':
    resolver()