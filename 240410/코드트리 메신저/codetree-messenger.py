# import sys
# import time
# sys.stdin = open("input.txt", "r")


class Node:
    def __init__(self, num, auth):
        self.num = num
        self.left = None
        self.right = None
        self.auth = auth
        self.alert = 1  # 0: off, 1: on

    def __repr__(self):
        # return f"[Node]num={self.num}, left={self.left.num if self.left is not None else None}, right={self.right.num if self.right is not None else None}"
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

    if parents[node1.num] == parents[node2.num]:
        return

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


# 알림 받을 수 있는 채팅방 수 조회
def check(target_node, node_list):
    global check_list
    for node, depth in node_list:
        if 0 < depth <= target_node.auth:
            check_list[node.num] += 1

    for i in range(len(node_list)):
        node_list[i][1] += 1

    if target_node.left is not None and target_node.left.alert == 1:
        node_list.append([target_node.left, 0])
        check(target_node.left, node_list)
        node_list.pop()

    if target_node.right is not None and target_node.right.alert == 1:
        node_list.append([target_node.right, 0])
        check(target_node.right, node_list)
        node_list.pop()

    for i in range(len(node_list)):
        node_list[i][1] -= 1


def check_list_clear():
    for i in range(len(check_list)):
        check_list[i] = 0

# start = time.time()

# 입력받기
N, Q = map(int, input().split(" "))
parents = [0]
authority = [0]
nodes = []
cnt = 0
check_list = [0] * (N + 1)

init_cmd = list(input().split(" "))
parents.extend(map(int, init_cmd[1:N + 1]))
authority.extend(map(int, init_cmd[N + 1:]))

# 초기화
initialize()
# end = time.time()
# print(f"time for init={end-start:.5f}sec")

# start = time.time()
# check(nodes[0], [[nodes[0], 0]])  # 방마다 알림을 받을 수 있는 채팅방 수 조회
# end = time.time()
# print(f"time for check={end-start:.5f}sec")

prev_cmd = None

# 명령어 실행
for _ in range(Q - 1):
    cmd = list(input().split())

    if cmd[0] == '200':
        c = int(cmd[1])
        toggle_alert(nodes[c])
    elif cmd[0] == '300':
        c, power = map(int, cmd[1:])
        change_auth(nodes[c], power)
    elif cmd[0] == '400':
        c1, c2 = map(int, cmd[1:])
        change_parent(nodes[c1], nodes[c2])
    else:
        if prev_cmd != '500':
            check_list_clear()
            check(nodes[0], [[nodes[0], 0]])  # 방마다 알림을 받을 수 있는 채팅방 수 조회
        c = int(cmd[1])
        print(check_list[c])

    prev_cmd = cmd[0]