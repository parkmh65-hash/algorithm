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
        steps.append({"index": i, "value": val})
        if val == req.target:
            found = True
            break
            
    return {
        "steps": steps,
        "found": found,
        "complexity": "O(N)"
    }
 
