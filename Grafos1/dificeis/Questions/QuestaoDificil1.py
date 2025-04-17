from collections import deque
import sys

def bfs_caminho_minimo(n, grafo, s):
    distancias = [-1] * (n + 1)
    distancias[s] = 0
    fila = deque([s])
    while fila:
        atual = fila.popleft()
        for vizinho in grafo[atual]:
            if distancias[vizinho] == -1:
                distancias[vizinho] = distancias[atual] + 6
                fila.append(vizinho)
    return distancias

def resolver():
    dados = sys.stdin.read().split()
    t = int(dados[0])
    idx = 1
    resultados = []
    for _ in range(t):
        n = int(dados[idx]); m = int(dados[idx+1])
        idx += 2
        grafo = [[] for _ in range(n + 1)]
        for __ in range(m):
            u = int(dados[idx]); v = int(dados[idx+1])
            idx += 2
            grafo[u].append(v)
            grafo[v].append(u)
        s = int(dados[idx]); idx += 1
        dist = bfs_caminho_minimo(n, grafo, s)
        res = []
        for i in range(1, n + 1):
            if i == s: continue
            res.append(str(dist[i]))
        resultados.append(" ".join(res))
    sys.stdout.write("\n".join(resultados))

if __name__ == '__main__':
    resolver()
