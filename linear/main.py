from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 보안을 위해 실제 운영 시에는 프론트엔드 도메인만 지정하세요.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

