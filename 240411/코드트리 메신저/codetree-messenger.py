class Node:
    def __init__(self, num, auth):
        self.num = num
        self.left = None
        self.right = None
        self.auth = auth
        self.alert = 1  # 0: off, 1: on

    def __repr__(self):
        return f"Node{self.num}"


# 초기화
def initialize():
    global parents, nodes, authority, N

    nodes.append(Node(0, 0))  # 메인 채팅방

    # 노드 만들기
    for i in range(1, N + 1):
        nodes.append(Node(i, authority[i]))

    # 트리 만들기
    for i in range(1, len(parents)):
        parent = nodes[parents[i]]
        node = nodes[i]

        if parent.left is None:
            parent.left = node
        else:
            parent.right = node

    # 초기 알림 수 계산
    for node in nodes:
        update_route_alert(node, 0, node.auth, 1, 1)


# 알림망 설정 토글
def toggle_alert(node):
    node.alert = abs(node.alert - 1)


# 권한 세기 변경
def change_auth(node, auth):
    node.auth = auth


# 부모 채팅방 교환
def change_parent(node1, node2):
    global parents, nodes
    parent1 = nodes[parents[node1.num]]
    parent2 = nodes[parents[node2.num]]

    # 부모 교환
    if parent1.left == node1 and parent2.left == node2:
        parent1.left = node2
        parent2.left = node1
    elif parent1.left == node1 and parent2.right == node2:
        parent1.left = node2
        parent2.right = node1
    elif parent1.right == node1 and parent2.left == node2:
        parent1.right = node2
        parent2.left = node1
    else:
        parent1.right = node2
        parent2.right = node1

    parents[node1.num] = parent2.num
    parents[node2.num] = parent1.num


def update_route_alert(node, start, end, gap, p):
    route = find_route(node)
    for i in range(min(start, len(route)-1), min(end, len(route)), gap):
        alert_num[route[i]] += p


def find_route(node):
    route = []
    while parents[node.num] != 0:
        route.append(parents[node.num])
        node = nodes[parents[node.num]]
    route.append(0)

    return route


def alert_dfs(node, depth, p):
    # 알림 토글 적용
    update_route_alert(node, depth, node.auth, 1, p)

    if node.left is not None:
        if node.left.alert == 1:
            alert_dfs(node.left, depth + 1, p)
        else:
            to_toggle.append(node.left)
    if node.right is not None:
        if node.right.alert == 1:
            alert_dfs(node.right, depth + 1, p)
        else:
            to_toggle.append(node.right)


# 노드에 변경이 생기면 채팅방 알림 수 업데이트
def update_alert_num(cmd):
    # 1. 알림 토글
    if cmd[0] == '200':
        node = nodes[int(cmd[1])]
        toggle_alert(node)
        if node.alert == 0:  # 꺼진 경우
            alert_dfs(node, 0, -1)
        else:
            alert_dfs(node, 0, 1)

    # 2. 권한 세기 변경
    elif cmd[0] == '300':
        new_auth = int(cmd[2])
        node = nodes[int(cmd[1])]
        if node.alert == 1:
            if node.auth < new_auth:  # 권한 증가
                update_route_alert(node, new_auth-1, new_auth-node.auth - 2, -1, 1)
            elif node.auth > new_auth:  # 권한 감소
                update_route_alert(node, new_auth-1, new_auth-node.auth - 2, -1, -1)
            change_auth(node, new_auth)

    # 3. 부모 채팅방 교환
    # 해당 노드들 경로 계산
    elif cmd[0] == '400':
        c1, c2 = map(int, cmd[1:])
        node1 = nodes[c1]
        node2 = nodes[c2]

        if parents[node1.num] == parents[node2.num]:
            return

        # 연결 끊기
        for node in [node1, node2]:
            if node.alert == 1:  # 알림 켜져 있으면 업데이트
                alert_dfs(node, 0, -1)

        # 부모 교환
        change_parent(node1, node2)

        # 알림 수 업데이트
        to_toggle.clear()
        for node in [node1, node2]:
            if node.alert == 0:
                to_toggle.append(node)
            alert_dfs(node, 0, 1)

        # 알림 오프 적용
        for node in to_toggle:
            alert_dfs(node, 0, -1)


# 입력 받기
N, Q = map(int, input().split(" "))
parents = [0]
authority = [0]
nodes = []
alert_num = [0] * (N + 1)
to_toggle = []

init_cmd = list(input().split(" "))
parents.extend(map(int, init_cmd[1:N + 1]))
authority.extend(map(int, init_cmd[N + 1:]))

# 초기화
initialize()

# 명령어 실행
for _ in range(Q - 1):
    cmd = list(input().split())

    if cmd[0] == '500':
        print(alert_num[int(cmd[1])])
    else:
        update_alert_num(cmd)