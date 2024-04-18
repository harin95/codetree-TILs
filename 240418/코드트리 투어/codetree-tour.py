import heapq
from collections import defaultdict

# 최소 거리 구하기
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

# 초기화
distance = run_dijkstra(0)
id_tf = [False] * 30001

# 여행상품 저장
product = []

for _ in range(Q-1):
    cmd = input().split()
    if cmd[0] == '200':     # 여행 상품 생성
        id, rev, dest = list(map(int, cmd[1:]))
        flag = -1 if distance[dest] == float("inf") else 0
        product.append([id, rev, dest, flag])
        id_tf[id] = True

    elif cmd[0] == '300':    # 여행 상품이 존재할 경우 취소
        id = int(cmd[1])
        if id_tf[id]:
            id_tf[id] = False

    elif cmd[0] == '400':
        if not product:
            print(-1)
        else:
            product.sort(key=lambda x: (x[3], x[1]-distance[x[2]], -x[0]))   # 수익 오름차순, 아이디 내림차순 (맨 뒤에서 뽑기 위해서 반대로)

            # 삭제된 경우
            while product and not id_tf[product[-1][0]]:
                product.pop()
            if not product:
                print(-1)

            # 도달하지 못하는 경우
            elif product[-1][3] == -1:
                print(-1)
            # 이득이 없는 경우
            elif product[-1][1] - distance[product[-1][2]] < 0:
                print(-1)
            else:   # 판매 가능
                res = product.pop()
                print(res[0])

    elif cmd[0] == '500':
        start = int(cmd[1])
        distance = run_dijkstra(start)
        for prod in product:
            prod[3] = -1 if distance[prod[2]] == float("inf") else 0    # 시작점 바뀌면 도달하지 못하는 경우 다시 계산