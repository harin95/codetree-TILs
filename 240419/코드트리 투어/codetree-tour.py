import heapq
from heapq import heapify
from collections import defaultdict


class Product:
    distance = []

    def __init__(self, id, rev, dest):
        self.id = id
        self.rev = rev
        self.dest = dest

    def __lt__(self, other):
        if self.rev - Product.distance[self.dest] > other.rev - Product.distance[other.dest]:   # 이익 내림차순
            return True
        elif self.rev - Product.distance[self.dest] == other.rev - Product.distance[other.dest]:  # id 오름차순
            return self.id < other.id


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
Product.distance = run_dijkstra(0)
id_tf = [False] * 30001

# 여행상품 저장
products = []

for _ in range(Q-1):
    cmd = input().split()
    if cmd[0] == '200':     # 여행 상품 생성
        id, rev, dest = list(map(int, cmd[1:]))
        heapq.heappush(products, Product(id, rev, dest))
        id_tf[id] = True

    elif cmd[0] == '300':    # 여행 상품이 존재할 경우 취소
        id = int(cmd[1])
        if id_tf[id]:
            id_tf[id] = False

    elif cmd[0] == '400':
        if not products:
            print(-1)
        else:
            res = heapq.heappop(products)
            heapq.heappush(products, res)
            res = products[0]

            # 삭제된 경우
            if not id_tf[res.id]:
                while products and not id_tf[res.id]:
                    res = heapq.heappop(products)
                    if id_tf[res.id]:
                        heapq.heappush(products, res)
            if not products:
                print(-1)

            # 도달하지 못하는 경우
            elif res.rev - Product.distance[res.dest] == float("-inf"):
                print(-1)

            # 이익이 나지 않는 경우
            elif id_tf[res.id] and res.rev - Product.distance[res.dest] < 0:
                print(-1)
            # 판매가능
            else:
                print(res.id)
                heapq.heappop(products)

    elif cmd[0] == '500':
        start = int(cmd[1])
        Product.distance = run_dijkstra(start)
        heapify(products)