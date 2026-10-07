from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# CORS(교차 출처 리소스 공유) 허용 설정 (모든 도메인 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. 노드 클래스
class Node:
    def __init__(self, key: int, value: str, next=None):
        self.key = key
        self.value = value
        self.next = next

# 2. 체인 해시 알고리즘 클래스
class ChainedHash:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.table = [None] * self.capacity

    def hash_value(self, key: int) -> int:
        return key % self.capacity

    def get_state(self):
        """현재 해시 테이블의 상태를 리스트로 반환 (시각화용)"""
        state = []
        for i in range(self.capacity):
            chain = []
            node = self.table[i]
            while node is not None:
                chain.append({"key": node.key, "value": node.value})
                node = node.next
            state.append(chain)
        return state

    def search(self, key: int):
        before = self.get_state()
        hash_idx = self.hash_value(key)
        steps = [{"msg": f"[해시계산] {key} % {self.capacity} = 인덱스 {hash_idx} 접근", "b_idx": hash_idx, "n_key": None}]
        
        node = self.table[hash_idx]
        while node is not None:
            steps.append({"msg": f"[비교] 노드 키 {node.key} 확인", "b_idx": hash_idx, "n_key": node.key})
            if node.key == key:
                steps.append({"msg": f"[성공] 값 '{node.value}' 찾음", "b_idx": hash_idx, "n_key": node.key, "found": True})
                return {"status": "검색 성공", "steps": steps, "complexity": "O(1) ~ O(N)", "before": before, "after": before}
            node = node.next
            
        steps.append({"msg": "[실패] 일치하는 키 없음", "b_idx": hash_idx, "n_key": None})
        return {"status": "검색 실패", "steps": steps, "complexity": "O(1) ~ O(N)", "before": before, "after": before}

    def add(self, key: int, value: str):
        before = self.get_state()
        hash_idx = self.hash_value(key)
        steps = [{"msg": f"[해시계산] {key} % {self.capacity} = 인덱스 {hash_idx} 접근", "b_idx": hash_idx, "n_key": None}]
        
        node = self.table[hash_idx]
        while node is not None:
            steps.append({"msg": f"[비교] 노드 키 {node.key} 중복 확인", "b_idx": hash_idx, "n_key": node.key})
            if node.key == key:
                steps.append({"msg": "[실패] 이미 존재하는 키", "b_idx": hash_idx, "n_key": node.key})
                return {"status": "추가 실패", "steps": steps, "complexity": "O(1) ~ O(N)", "before": before, "after": before}
            node = node.next
            
        self.table[hash_idx] = Node(key, value, self.table[hash_idx])
        steps.append({"msg": f"[성공] 리스트 맨 앞에 {key}:{value} 추가됨", "b_idx": hash_idx, "n_key": key})
        return {"status": "추가 성공", "steps": steps, "complexity": "O(1)", "before": before, "after": self.get_state()}

    def remove(self, key: int):
        before = self.get_state()
        hash_idx = self.hash_value(key)
        steps = [{"msg": f"[해시계산] {key} % {self.capacity} = 인덱스 {hash_idx} 접근", "b_idx": hash_idx, "n_key": None}]
        
        node = self.table[hash_idx]
        prev = None
        
        while node is not None:
            steps.append({"msg": f"[비교] 노드 키 {node.key} 확인", "b_idx": hash_idx, "n_key": node.key})
            if node.key == key:
                if prev is None:
                    self.table[hash_idx] = node.next
                else:
                    prev.next = node.next
                steps.append({"msg": f"[성공] 키 {key} 삭제 완료", "b_idx": hash_idx, "n_key": None})
                return {"status": "삭제 성공", "steps": steps, "complexity": "O(1) ~ O(N)", "before": before, "after": self.get_state()}
            prev = node
            node = node.next
            
        steps.append({"msg": "[실패] 삭제할 키 없음", "b_idx": hash_idx, "n_key": None})
        return {"status": "삭제 실패", "steps": steps, "complexity": "O(1) ~ O(N)", "before": before, "after": before}

    def dump(self):
        state = self.get_state()
        return {"status": "덤프 완료", "steps": [{"msg": "[완료] 전체 해시 테이블 상태 출력", "b_idx": -1, "n_key": None}], "complexity": "O(N)", "before": state, "after": state}


# 시각화를 위해 capacity를 5로 설정한 전역 해시 테이블
hash_db = ChainedHash(5)

class HashReq(BaseModel):
    action: str
    key: Optional[int] = 0
    value: Optional[str] = ""

@app.post("/hash-api")
def hash_api(req: HashReq):
    if req.action == "add": return hash_db.add(req.key, req.value)
    if req.action == "search": return hash_db.search(req.key)
    if req.action == "remove": return hash_db.remove(req.key)
    if req.action == "dump": return hash_db.dump()
