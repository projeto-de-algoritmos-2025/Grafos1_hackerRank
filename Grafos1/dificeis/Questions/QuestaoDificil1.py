def main():
    dados = sys.stdin.read().split()
    t = int(dados[0])
    indice = 1
    resultados = []
    for _ in range(t):
        n = int(dados[indice])
        m = int(dados[indice + 1])
        indice += 2
        grafo = [[] for _ in range(n + 1)]
        for _ in range(m):
            u = int(dados[indice])
            v = int(dados[indice + 1])
            indice += 2
            grafo[u].append(v)
            grafo[v].append(u)
        s = int(dados[indice])
        indice += 1
        distancias = bfs_caminho_minimo(n, grafo, s)
        res = []
        for i in range(1, n + 1):
            if i == s:
                continue
            res.append(str(distancias[i]))
        resultados.append(" ".join(res))
    sys.stdout.write("\n".join(resultados))

if __name__ == '__main__':
    main()