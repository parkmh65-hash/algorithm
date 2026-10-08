# Python 3.10 경량 이미지 사용
FROM python:3.10-slim

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# 의존성 패키지 설치 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Cloud Run 기본 포트(8080) 설정 및 Gunicorn 서버 실행
ENV PORT=8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
