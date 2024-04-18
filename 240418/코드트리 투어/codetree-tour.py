import heapq
from collections import defaultdict
# import sys
# sys.stdin = open("input.txt", "r")


def run_dijkstra(start):
    distance = [float("inf")] * n
    distance[start] = 0

    pq = []
    heapq.heappush(pq, [0, start])

    while pq:
        cur = heapq.heappop(pq)
        cur_num = cur[1]
        cur_cost = distance[cur_num]

        if not edges.get(cur_num):
            continue

        for edge in edges.get(cur_num):
            next_cost = cur_cost + edge[0]
            next_num = edge[1]

            if distance[next_num] > next_cost:
                distance[next_num] = next_cost
                heapq.heappush(pq, (next_cost, next_num))

    return distance


Q = int(input())

cmd = list(map(int, input().split()))
n, m, info = cmd[1], cmd[2], cmd[3:]
edges = defaultdict(list)

for i in range(0, (m-1)*3+1, 3):
    fr = info[i]
    to = info[i+1]
    cost = info[i+2]
    # 양방향 간선 저장
    edges[fr].append([cost, to])
    edges[to].append([cost, fr])

# init
distance = run_dijkstra(0)
id_tf = [False] * 30001

product = []

for _ in range(Q-1):
    cmd = input().split()
    if cmd[0] == '200':
        id, rev, dest = list(map(int, cmd[1:]))
        inf_flag = -1 if distance[dest] == float("inf") else 0
        product.append([id, rev, dest, inf_flag])
        id_tf[id] = True
    elif cmd[0] == '300':
        id = int(cmd[1])
        id_tf[id] = False
    elif cmd[0] == '400':
        if not product:
            print(-1)
        else:
            product.sort(key=lambda x: (inf_flag, x[1]-distance[x[2]], -x[0]))   # 수익 오름차순, 아이디 내림차순
            # 도달하지 못하는 경우
            if product[-1][3] == -1:
                print(-1)
            # 삭제된 경우
            elif not id_tf[product[-1][0]]:
                product.pop()
                print(-1)
            # 이득이 없는 경우
            elif product[-1][1] - distance[product[-1][2]] < 0:
                print(-1)
            else:
                res = product.pop()
                print(res[0])

    elif cmd[0] == '500':
        start = int(cmd[1])
        distance = run_dijkstra(start)
        for prod in product:
            prod[3] = -1 if distance[prod[2]] == float("inf") else 0