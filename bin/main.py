from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    arr: list[int]
    target: int

@app.post("/binary-search")
def binary_search(req: SearchRequest):
    steps = []
    left, right = 0, len(req.arr) - 1
    found = False
    
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
