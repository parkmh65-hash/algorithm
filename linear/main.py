from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SearchReq(BaseModel):
    arr: list[int]
    target: int

@app.post("/linear-search")
def linear_search(req: SearchReq):
    steps = []
    for i, val in enumerate(req.arr):
        steps.append(f"인덱스 {i} 확인: {val}")
        if val == req.target:
            return {"steps": steps, "found": True, "count": i + 1, "complexity": "O(N)"}
    return {"steps": steps, "found": False, "count": len(req.arr), "complexity": "O(N)"}
