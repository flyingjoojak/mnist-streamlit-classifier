# 🖌️ MNIST 손글씨 인식 웹 서비스

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40.0-red)
![ONNX](https://img.shields.io/badge/ONNX-Runtime-lightgrey)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

사용자가 웹 캔버스에 직접 쓴 숫자를 인공지능(ONNX) 모델이 실시간으로 인식하여 예측 결과를 보여주는 웹 애플리케이션입니다.

## 📌 주요 기능

1.  **실시간 손글씨 인식**:
    *   사용자가 마우스나 터치로 숫자를 그리면 즉시 분석합니다.
    *   `streamlit-drawable-canvas` 라이브러리를 활용하여 직관적인 그리기 인터페이스를 제공합니다.

2.  **이미지 전처리 및 시각화**:
    *   입력된 그림을 MNIST 모델 학습 데이터와 동일한 형식(28x28 Grayscale)으로 자동 변환합니다.
    *   전처리된 이미지를 화면에 표시하여 모델이 보고 있는 데이터를 사용자가 확인할 수 있습니다.

3.  **AI 모델 추론 및 결과 분석**:
    *   ONNX Runtime을 사용하여 경량화된 추론 엔진을 구동합니다.
    *   0부터 9까지 각 숫자에 대한 예측 확률을 막대 그래프로 시각화하여 보여줍니다.

4.  **히스토리 관리**:
    *   사용자가 '결과 저장하기' 버튼을 누르면 현재 예측 결과와 이미지를 세션에 저장합니다.
    *   하단 갤러리 영역에서 저장된 기록들을 최근 순서대로 확인할 수 있습니다.

## 🛠️ 기술 스택

*   **Language**: Python 3.9
*   **Web Framework**: Streamlit
*   **AI/ML**: ONNX Runtime, NumPy, OpenCV
*   **Containerization**: Docker

## 📂 프로젝트 구조

```bash
📦 mission-mnist
 ┣ 📂 utils
 ┃ ┣ 📜 model_loader.py    # ONNX 모델 다운로드 및 로딩 (캐싱 적용)
 ┃ ┗ 📜 preprocessing.py   # 이미지 전처리 (Resize, Grayscale, Normalize)
 ┣ 📜 app.py               # 메인 Streamlit 애플리케이션
 ┣ 📜 Dockerfile           # Docker 빌드 설정 파일
 ┣ 📜 requirements.txt     # 프로젝트 의존성 목록
 ┗ 📜 README.md            # 프로젝트 설명 문서
```

## 🚀 설치 및 실행 방법

### 1. 로컬 환경에서 실행

1.  **저장소 클론 및 이동**
    ```bash
    git clone [repository-url]
    cd [project-folder]
    ```

2.  **패키지 설치**
    ```bash
    pip install -r requirements.txt
    ```

3.  **애플리케이션 실행**
    ```bash
    streamlit run app.py
    ```

### 2. Docker로 실행

1.  **Docker 이미지 빌드**
    ```bash
    docker build -t mnist-streamlit .
    ```

2.  **컨테이너 실행**
    ```bash
    docker run -p 8501:8501 mnist-streamlit
    ```
    *   브라우저에서 `http://localhost:8501` 접속

## 🐳 Docker Hub

이 프로젝트는 Docker Hub에도 배포되어 있습니다. 아래 명령어로 바로 실행해볼 수 있습니다.

```bash
docker pull joojak0616/mnist-streamlit:latest
docker run -p 8501:8501 joojak0616/mnist-streamlit:latest
```

## 📝 개발 후기 & 배운 점

*   **Streamlit 활용**: 복잡한 프론트엔드 코드 없이 Python만으로 인터랙티브한 대시보드를 빠르게 구축하는 경험을 했습니다.
*   **ONNX Runtime**: 학습된 모델을 효율적으로 배포하기 위해 ONNX 포맷을 활용하고, `st.cache_resource`를 통해 모델 로딩 시간을 최적화했습니다.
*   **Docker Containerization**: 개발 환경과 배포 환경의 일관성을 유지하기 위해 Docker를 도입하고, 실제로 이미지를 빌드하여 Docker Hub에 배포하는 전체 CI/CD 파이프라인의 기초를 다졌습니다.

---
**Author**: 주재홍 (Team 4)
