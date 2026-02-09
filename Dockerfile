FROM python:3.9-slim

WORKDIR /app

# 필수 패키지 설치를 위한 requirements 복사
COPY requirements.txt .

# 패키지 설치
# opencv-python-headless 의존성을 위해 libgl1-mesa-glx 등이 필요할 수 있으나,
# headless 버전은 보통 추가 시스템 라이브러리 없이도 동작하는 경우가 많음.
# 만약 ImportError: libGL.so.1... 에러 발생 시 아래 apt-get 라인 주석 해제하여 사용.
# RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Streamlit 포트 노출
EXPOSE 8501

# 실행 명령어
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
