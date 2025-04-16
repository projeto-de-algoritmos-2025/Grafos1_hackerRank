
import math
import os
import random
import re
import sys
from collections import deque, defaultdict

def bfs(capacity, graph, source, sink, parent):
    visited = set()
    queue = deque([source])
    visited.add(source)

    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in visited and capacity[u][v] > 0:
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return True
                queue.append(v)
    return False

def crabGraphs(n, t, graph):
    from collections import defaultdict, deque

    N = 2 * n + 2
    source = 0
    sink = N - 1

    capacity = [[0] * N for _ in range(N)]
    adj = [[] for _ in range(N)]

    # For each vertex v (1..n)
    for v in range(1, n + 1):
        # source -> v (head node): capacity T
        capacity[source][v] = t
        adj[source].append(v)
        adj[v].append(source)

        # v' (foot node) -> sink: capacity 1
        capacity[v + n][sink] = 1
        adj[v + n].append(sink)
        adj[sink].append(v + n)

    # For each edge (u, v)
    for u, v in graph:
        # Connect u (head) -> v' (foot)
        capacity[u][v + n] = 1
        adj[u].append(v + n)
        adj[v + n].append(u)

        # Connect v (head) -> u' (foot)
        capacity[v][u + n] = 1
        adj[v].append(u + n)
        adj[u + n].append(v)

    # Edmonds-Karp
    def bfs(parents):
        visited = [False] * N
        queue = deque()
        queue.append(source)
        visited[source] = True

        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if not visited[v] and capacity[u][v] > 0:
                    visited[v] = True
                    parents[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
        return False

    def edmonds_karp():
        flow = 0
        parents = [-1] * N

        while bfs(parents):
            path_flow = float('inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, capacity[parents[s]][s])
                s = parents[s]

            flow += path_flow
            v = sink
            while v != source:
                u = parents[v]
                capacity[u][v] -= path_flow
                capacity[v][u] += path_flow
                v = u
        return flow

    return edmonds_karp()


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    c = int(input().strip())

    for c_itr in range(c):
        first_multiple_input = input().rstrip().split()

        n = int(first_multiple_input[0])
        t = int(first_multiple_input[1])
        m = int(first_multiple_input[2])

        graph = []

        for _ in range(m):
            graph.append(list(map(int, input().rstrip().split())))

        result = crabGraphs(n, t, graph)

        fptr.write(str(result) + '\n')

    fptr.close()
