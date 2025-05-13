# Сюда отправляем решение задачи "Лабиринт с дверьми"
# Подумайте, как можно моделировать двери, используя существующие алгоритмы работы с графами.


# Решите задачу и выведите ответ в нужном формате
graph = [
    [1],  # 0
    [0, 5],  # 1
    [6],  # 2
    [7],  # 3  s-3
    [8],  # 4D
    [1],  # 5D s-1
    [2, 10],  # 6
    [3, 11],  # 7
    [4, 9, 12],   #8  s-4
    [8, 10], #9
    [6, 9], # 10
    [7, 15], # 11
    [8], # 12D
    [], # 13D  s-2
    [], # 14D
    [11], # 15D
]
graph_open_door = [
    [1],  # 0
    [0, 5],  # 1
    [6],  # 2
    [7],  # 3  s-3
    [8,5],  # 4D
    [1,4],  # 5D s-1
    [2, 10],  # 6
    [3, 11],  # 7
    [4, 9, 12],   #8 s-4
    [8, 10], #9
    [6, 9], # 10
    [7, 15], # 11
    [8,13], # 12D
    [12], # 13D s-2
    [15], # 14D
    [11,14], # 15D
]
objects_start = {
    '1': 5,
    '2': 13,  #13
    '3': 3,
    '4': 8,
}
key = [7 , 10]
finish = [0]

def dfs(graph, start):
    visited = [False] * len(graph)
    def _dfs(v):
        visited[v] = True
        for w in graph[v]:
            if not visited[w]:  # посещён ли текущий сосед?
                _dfs(w)

    _dfs(start)
    return visited

for name, start in objects_start.items():
    result = dfs(graph, start)
    can_take_key = any(result[k] for k in key)
    if can_take_key:
        result = dfs(graph_open_door, start)
        if result[finish[0]]:
            print(f"Из точки S-{name} можно добраться до финиша, используя ключ")
            continue
        else:
            print(f"Из точки S-{name} нельзя добраться до финиша")
            continue
    if result[finish[0]]:
        print(f"Из точки S-{name} можно добраться до финиша без ключа")
    else:
        print(f"Из точки S-{name} нельзя добраться до финиша")
