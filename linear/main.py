# main.py
from flask import Flask, request, jsonify

app = Flask(__name__)

def linear_search_steps(arr, target):
    """
    선형 검색(Linear Search) 알고리즘을 수행하고,
    각 단계별 탐색 과정과 결과를 리스트로 반환합니다.
    
    시간 복잡도: $O(N)$
    공간 복잡도: $O(1)$ (결과 저장용 리스트 제외)
    """
    steps = []
    found_index = -1
    
    for i in range(len(arr)):
        current_value = arr[i]
        is_match = (current_value == target)
        
        # 현재 단계의 검사 상태 기록
        steps.append({
            "step": i + 1,
            "index": i,
            "value": current_value,
            "matched": is_match,
            "message": f"인덱스 [{i}]의 값({current_value})과 목표값({target})을 비교합니다."
        })
        
        if is_match:
            found_index = i
            break
            
    return {
        "array": arr,
        "target": target,
        "found_index": found_index,
        "steps": steps,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)"
    }

@app.route('/search', methods=['POST'])
def search():
    """
    클라이언트로부터 배열과 타겟값을 받아 선형 검색을 수행하는 API 엔드포인트
    """
    try:
        data = request.get_json()
        arr = data.get('array', [12, 34, 56, 78, 90])
        target = data.get('target', 78)
        
        # 선형 검색 알고리즘 실행
        result = linear_search_steps(arr, target)
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/health', methods=['GET'])
def health_check():
    """서버 정상 작동 여부를 확인하는 헬스체크 엔드포인트"""
    return jsonify({"status": "healthy", "service": "linear-search-server"}), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
