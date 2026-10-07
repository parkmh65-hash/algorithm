from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# CORS 교차 출처 리소스 공유 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. 노드 클래스
class Node:
    def __init__(self, key: int, value: str):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

# 2. 이진 검색 트리 클래스
class BinarySearchTree:
    def __init__(self):
        self.root = None

    def get_state(self, node):
        """현재 트리의 구조를 JSON 형태(딕셔너리)로 직렬화하여 반환"""
        if node is None:
            return None
        return {
            "key": node.key,
            "value": node.value,
            "left": self.get_state(node.left),
            "right": self.get_state(node.right)
        }

    def search(self, key: int):
        state = self.get_state(self.root)
        steps = [{"msg": f"검색 시작: 키 {key}", "h_key": None}]
        p = self.root
        
        while p is not None:
            steps.append({"msg": f"[비교] 노드 {p.key} 확인", "h_key": p.key})
            if key == p.key:
                steps.append({"msg": f"[성공] 값 '{p.value}' 찾음!", "h_key": p.key})
                return {"status": "검색 성공", "steps": steps, "complexity": "O(log N)", "before": state, "after": state}
            elif key < p.key:
                steps.append({"msg": f"[이동] {key} < {p.key} 이므로 왼쪽으로 이동", "h_key": p.key})
                p = p.left
            else:
                steps.append({"msg": f"[이동] {key} > {p.key} 이므로 오른쪽으로 이동", "h_key": p.key})
                p = p.right
                
        steps.append({"msg": "[실패] 일치하는 키가 트리 안에 없습니다.", "h_key": None})
        return {"status": "검색 실패", "steps": steps, "complexity": "O(log N)", "before": state, "after": state}

    def add(self, key: int, value: str):
        before = self.get_state(self.root)
        steps = [{"msg": f"추가 시작: {key}", "h_key": None}]
        
        if self.root is None:
            self.root = Node(key, value)
            steps.append({"msg": f"[성공] 루트 노드로 {key} 추가됨", "h_key": key})
            return {"status": "추가 성공", "steps": steps, "complexity": "O(1)", "before": before, "after": self.get_state(self.root)}
            
        p = self.root
        while True:
            steps.append({"msg": f"[비교] 노드 {p.key} 확인", "h_key": p.key})
            if key == p.key:
                steps.append({"msg": "[실패] 이미 존재하는 키입니다.", "h_key": p.key})
                return {"status": "추가 실패", "steps": steps, "complexity": "O(log N)", "before": before, "after": before}
            elif key < p.key:
                if p.left is None:
                    p.left = Node(key, value)
                    steps.append({"msg": f"[성공] {p.key}의 왼쪽 자식으로 추가됨", "h_key": key})
                    break
                steps.append({"msg": f"[이동] 왼쪽 서브트리로 이동", "h_key": p.key})
                p = p.left
            else:
                if p.right is None:
                    p.right = Node(key, value)
                    steps.append({"msg": f"[성공] {p.key}의 오른쪽 자식으로 추가됨", "h_key": key})
                    break
                steps.append({"msg": f"[이동] 오른쪽 서브트리로 이동", "h_key": p.key})
                p = p.right
                
        return {"status": "추가 성공", "steps": steps, "complexity": "O(log N)", "before": before, "after": self.get_state(self.root)}

    def remove(self, key: int):
        before = self.get_state(self.root)
        steps = [{"msg": f"삭제 시작: {key}", "h_key": None}]
        
        p = self.root
        parent = None
        is_left_child = False

        # 1. 삭제할 노드 탐색
        while p is not None:
            steps.append({"msg": f"[비교] 노드 {p.key} 확인", "h_key": p.key})
            if key == p.key:
                break
            parent = p
            if key < p.key:
                is_left_child = True
                p = p.left
            else:
                is_left_child = False
                p = p.right
                
        if p is None:
            steps.append({"msg": "[실패] 삭제할 키가 없습니다.", "h_key": None})
            return {"status": "삭제 실패", "steps": steps, "complexity": "O(log N)", "before": before, "after": before}

        # 2. 자식 개수에 따른 삭제 로직
        if p.left is None and p.right is None:
            # 단말 노드
            if p == self.root: self.root = None
            elif is_left_child: parent.left = None
            else: parent.right = None
            steps.append({"msg": f"[성공] 단말 노드 {key} 삭제 완료", "h_key": key})
            
        elif p.left is None:
            # 오른쪽 자식만 존재
            if p == self.root: self.root = p.right
            elif is_left_child: parent.left = p.right
            else: parent.right = p.right
            steps.append({"msg": f"[성공] 오른쪽 자식이 있는 노드 {key} 삭제 완료", "h_key": key})
            
        elif p.right is None:
            # 왼쪽 자식만 존재
            if p == self.root: self.root = p.left
            elif is_left_child: parent.left = p.left
            else: parent.right = p.left
            steps.append({"msg": f"[성공] 왼쪽 자식이 있는 노드 {key} 삭제 완료", "h_key": key})
            
        else:
            # 두 자식이 모두 존재 -> 오른쪽 서브트리의 최소값으로 대체
            steps.append({"msg": f"[탐색] 두 자식이 존재. 오른쪽 서브트리에서 최소값 탐색", "h_key": p.key})
            parent_min = p
            min_node = p.right
            is_left_min = False
            
            while min_node.left is not None:
                parent_min = min_node
                min_node = min_node.left
                is_left_min = True
                
            steps.append({"msg": f"[대체] {p.key} 노드를 최소값 {min_node.key}로 덮어씀", "h_key": min_node.key})
            p.key = min_node.key
            p.value = min_node.value
            
            if is_left_min: parent_min.left = min_node.right
            else: parent_min.right = min_node.right
            steps.append({"msg": "[성공] 삭제 및 대체 완료", "h_key": p.key})

        return {"status": "삭제 성공", "steps": steps, "complexity": "O(log N)", "before": before, "after": self.get_state(self.root)}

    def min_key(self):
        state = self.get_state(self.root)
        steps = [{"msg": "최소값 탐색 시작 (가장 왼쪽 아래 노드)", "h_key": None}]
        if self.root is None:
            steps.append({"msg": "트리가 비어있습니다.", "h_key": None})
            return {"status": "탐색 실패", "steps": steps, "complexity": "O(1)", "before": state, "after": state}
            
        p = self.root
        while p.left is not None:
            steps.append({"msg": f"[이동] {p.key}의 왼쪽으로 이동", "h_key": p.key})
            p = p.left
        steps.append({"msg": f"[성공] 트리 최소값은 {p.key} 입니다.", "h_key": p.key})
        return {"status": "탐색 성공", "steps": steps, "complexity": "O(log N)", "before": state, "after": state}

    def max_key(self):
        state = self.get_state(self.root)
        steps = [{"msg": "최대값 탐색 시작 (가장 오른쪽 아래 노드)", "h_key": None}]
        if self.root is None:
            steps.append({"msg": "트리가 비어있습니다.", "h_key": None})
            return {"status": "탐색 실패", "steps": steps, "complexity": "O(1)", "before": state, "after": state}
            
        p = self.root
        while p.right is not None:
            steps.append({"msg": f"[이동] {p.key}의 오른쪽으로 이동", "h_key": p.key})
            p = p.right
        steps.append({"msg": f"[성공] 트리 최대값은 {p.key} 입니다.", "h_key": p.key})
        return {"status": "탐색 성공", "steps": steps, "complexity": "O(log N)", "before": state, "after": state}

    def dump(self):
        state = self.get_state(self.root)
        steps = [{"msg": "[덤프] 트리의 구조를 반환합니다.", "h_key": None}]
        return {"status": "덤프 완료", "steps": steps, "complexity": "O(N)", "before": state, "after": state}


# 전역 BST 초기화 및 샘플 데이터 삽입 (시각화 테스트용)
bst_db = BinarySearchTree()
for k, v in [(30, "A"), (15, "B"), (50, "C"), (10, "D"), (20, "E"), (40, "F")]:
    bst_db.add(k, v)

class BSTReq(BaseModel):
    action: str
    key: Optional[int] = 0
    value: Optional[str] = ""

@app.post("/bst-api")
def bst_api(req: BSTReq):
    if req.action == "add": return bst_db.add(req.key, req.value)
    if req.action == "search": return bst_db.search(req.key)
    if req.action == "remove": return bst_db.remove(req.key)
    if req.action == "min": return bst_db.min_key()
    if req.action == "max": return bst_db.max_key()
    if req.action == "dump": return bst_db.dump()
