class Node:
    def __init__(self, num):
        self.num = num
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node{self.num}"


def update_alert_num(node, p):
    global alert_num
    route = find_route(node)
    for i in route:
        alert_num[i] += p
        if not alert_tf[i]:
            break


# 초기화
def initialize():
    global parents, nodes, authority, N

    nodes.append(Node(0))  # 메인 채팅방

    # 노드 만들기
    for i in range(1, N + 1):
        nodes.append(Node(i))

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
        update_alert_num(node, 1)


# 부모 채팅방 교환
def change_parent(node1, node2):
    global parents, nodes
    parent1 = nodes[parents[node1.num]]
    parent2 = nodes[parents[node2.num]]

    # 부모 연결 교환
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

    # 부모 배열 업데이트
    parents[node1.num] = parent2.num
    parents[node2.num] = parent1.num


# node가 알림 전달하는 상위 루트 구하기
def find_route(node):
    global authority, parents
    auth = min(authority[node.num], 20)
    route = []
    while auth > 0:
        if parents[node.num] == -1:
            break
        route.append(parents[node.num])
        node = nodes[parents[node.num]]
        auth -= 1

    return route


def get_children_for_toggle(node):
    global toggle_children

    toggle_children.append(node)

    if node.left is not None and alert_tf[node.left.num]:
        get_children_for_toggle(node.left)
    if node.right is not None and alert_tf[node.right.num]:
        get_children_for_toggle(node.right)


def get_children_and_off(node):
    global children, off_list

    children.append(node)

    if not alert_tf[node.num]:
        off_list.append(node)

    if node.left is not None:
        get_children_and_off(node.left)
    if node.right is not None:
        get_children_and_off(node.right)


# 노드에 변경이 생기면 채팅방 알림 수 업데이트
def command(cmd):
    global children, off_list, alert_tf, authority
    # 1. 알림 토글
    if cmd[0] == '200':
        node = nodes[int(cmd[1])]
        alert_tf[node.num] = not alert_tf[node.num]     # toggle

        if not alert_tf[node.num]:
            update_alert_num(node, -1)
            toggle_children.clear()
            get_children_for_toggle(node)

            for temp_node in toggle_children:
                try:
                    route = find_route(temp_node)
                    idx = route.index(node.num)+1
                    for i in route[idx:]:
                        alert_num[i] -= 1
                        if not alert_tf[i]:
                            break
                except ValueError or IndexError:
                    continue

        else:
            update_alert_num(node, 1)
            toggle_children.clear()
            get_children_for_toggle(node)

            for temp_node in toggle_children:
                try:
                    route = find_route(temp_node)
                    idx = route.index(node.num)+1
                    for i in route[idx:]:
                        alert_num[i] += 1
                        if not alert_tf[i]:
                            break
                except ValueError or IndexError:
                    continue


    # 2. 권한 세기 변경
    elif cmd[0] == '300':
        new_auth = int(cmd[2])
        node = nodes[int(cmd[1])]
        if alert_tf[node.num]:
            update_alert_num(node, -1)
            authority[node.num] = new_auth
            update_alert_num(node, 1)
        else:
            authority[node.num] = new_auth

    # 3. 부모 채팅방 교환
    # 해당 노드들 경로 계산
    elif cmd[0] == '400':
        c1, c2 = map(int, cmd[1:])
        node1 = nodes[c1]
        node2 = nodes[c2]

        if parents[node1.num] == parents[node2.num]:
            return

        children.clear()
        off_list.clear()

        get_children_and_off(node1)     # 하위 경로 구하기
        get_children_and_off(node2)

        for node in off_list:   # 알림 꺼진 노드 알림 킴
            command(["200", node.num])

        for node in children:
            update_alert_num(node, -1)  # 연결 끊기

        change_parent(node1, node2)

        # 바뀐 부모랑 연결
        for node in children:
            update_alert_num(node, 1)

        # 알림 끄기 적용
        for node in off_list:
            command(["200", node.num])


# 입력 받기
N, Q = map(int, input().split(" "))
parents = [-1]
authority = [0]
alert_tf = [True] * (N+1)
nodes = []
alert_num = [0] * (N + 1)

children = []
off_list = []

toggle_children = []

init_cmd = list(input().split(" "))
parents.extend(map(int, init_cmd[1:N + 1]))
authority.extend(map(int, init_cmd[N + 1:]))

# 초기화
initialize()
cnt = 1
# 명령어 실행
for _ in range(Q - 1):
    cmd = list(input().split())

    if cmd[0] == '500':
        print(alert_num[int(cmd[1])])
    else:
        command(cmd)