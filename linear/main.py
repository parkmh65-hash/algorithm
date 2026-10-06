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
