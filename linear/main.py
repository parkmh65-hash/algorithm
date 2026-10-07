from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SearchRequest(BaseModel):
    arr: list[int]
    target: int

@app.post("/linear-search")
def linear_search(req: SearchRequest):
    steps = []
    found = False
    for i, val in enumerate(req.arr):
        match = (val == req.target)
        steps.append({"index": i, "value": val, "match": match})
        if match:
            found = True
            break
            
    return {
        "steps": steps,
        "found": found,
        "total_steps": len(steps),
        "complexity": "O(N)"
    }
    
@app.post("/binary-search")
def binary_search(req: SearchRequest):
    steps = []
    found = False
    left, right = 0, len(req.arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        val = req.arr[mid]
        steps.append({"left": left, "right": right, "mid": mid, "value": val})
        
        if val == req.target:
            found = True
            break
        elif val < req.target:
            left = mid + 1
        else:
            right = mid - 1
            
    return {
        "arr": req.arr,
        "target": req.target,
        "steps": steps,
        "found": found,
        "complexity": "O(log N)"
    }
