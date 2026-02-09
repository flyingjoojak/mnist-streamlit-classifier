# 🖌️ MNIST 기반 실시간 손글씨 인식 웹 서비스 (2025.01)

> **"사용자가 웹상에서 직접 쓴 숫자를 즉시 인식하고 분석하는 인터랙티브 AI 웹 애플리케이션"**

![Python](https://img.shields.io/badge/Python-3.9-blue?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40.0-red?style=flat-square&logo=streamlit&logoColor=white)
![ONNX](https://img.shields.io/badge/ONNX-Runtime-lightgrey?style=flat-square&logo=onnx&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=flat-square&logo=docker&logoColor=white)

---

### 1. 프로젝트 개요
**Situation (문제 정의):**
기존의 머신러닝 학습 모델들은 대부분 정적인 주피터 노트북 환경에서만 실행되어, 실제 사용자가 모델의 성능을 체감하거나 서비스를 경험하기 어려운 한계가 있었습니다. "어떻게 하면 비전문가도 쉽게 AI 모델을 테스트해볼 수 있을까?"라는 고민에서 출발했습니다.

**Task (목표):**
사용자가 웹 브라우저에서 마우스로 직접 숫자를 그리면, 백엔드의 AI 모델이 이를 실시간으로 분석하여 예측 결과를 시각적으로 보여주는 **End-to-End 웹 서비스**를 구축하는 것을 목표로 했습니다. 또한, 어디서든 배포 가능하도록 컨테이너화(Docker)까지 수행해야 했습니다.

---

### 2. 주요 역할 및 기술적 의사결정
*   **Streamlit 선정**: 복잡한 프론트엔드(React, Vue) 개발 비용을 최소화하고, Python 코드만으로 데이터 시각화와 인터랙티브 UI를 빠르게 구축하기 위해 선택했습니다. `streamlit-drawable-canvas` 라이브러리를 도입하여 사용자 입력(드로잉) 인터페이스를 구현했습니다.
*   **ONNX Runtime 도입**: PyTorch나 TensorFlow와 같은 무거운 딥러닝 프레임워크 전체를 서빙 환경에 올리는 것은 비효율적이라고 판단했습니다. 모델을 경량화된 ONNX 포맷으로 변환하고, `onnxruntime` 엔진을 사용하여 추론 속도를 최적화했습니다.
*   **Docker Containerization**: 로컬 개발 환경(Windows)과 배포 환경(Linux)의 차이로 인한 `Dependency Hell` 문제를 방지하기 위해 Docker를 도입했습니다. `Python 3.9-slim` 기반의 경량 이미지를 사용하여 빌드 속도와 저장 용량을 효율화했습니다.

---

### 3. 기술적 난관 및 해결 과정 (Troubleshooting)

#### 🚀 Issue 1: 사용자 입력 이미지와 모델 학습 데이터의 불일치
**문제점:**
사용자가 캔버스에 그린 그림은 흰 배경에 검은 획(또는 투명 배경)인 반면, MNIST 모델이 학습한 데이터는 검은 배경에 흰 획(Grayscale 28x28)이었습니다. 이로 인해 모델의 예측 정확도가 현저히 떨어지는 현상이 발생했습니다.

**해결 방안:**
`utils/preprocessing.py` 모듈을 직접 구현하여 데이터 파이프라인을 구축했습니다.
1.  **채널 변환**: RGBA 입력 이미지를 읽어들여 Alpha 채널을 분석하고, 배경과 전경을 분리하여 Grayscale로 변환했습니다.
2.  **색상 반전 및 정규화**: 학습 데이터 분포에 맞게 픽셀 값을 반전시키고 0~1 사이의 Float32 값으로 정규화(Normalization)했습니다.
3.  **차원 확장**: 모델의 입력 텐서 형태인 `(Batch, Channel, Height, Width)`에 맞춰 차원을 확장(`np.expand_dims`)했습니다.

**결과:**
전처리 로직 적용 전 10% 미만의 정확도에서, 적용 후 **90% 이상의 예측 정확도**를 달성했습니다.

#### ⚡ Issue 2: 매번 반복되는 모델 로딩으로 인한 지연
**문제점:**
사용자가 그림을 그리고 분석을 요청할 때마다 ONNX 모델 파일을 디스크에서 다시 읽어오는 오버헤드가 발생하여 응답 속도가 느려졌습니다.

**해결 방안:**
Streamlit의 캐싱 메커니즘인 `@st.cache_resource` 데코레이터를 활용했습니다.
*   애플리케이션 시작 시 모델을 한 번만 로드하여 메모리에 상주시켰습니다.
*   이후 요청부터는 캐시된 세션을 재사용하도록 구조를 개선했습니다.

**결과:**
추론 요청 시 모델 로딩 시간을 완전히 제거하여 **실시간에 가까운 응답성**을 확보했습니다.

---

### 4. 성과 및 배운 점
*   **정량적 성과**: Docker 이미지 크기를 최적화하여 500MB 미만으로 경량화하였으며, 로컬 PC뿐만 아니라 어떤 환경에서도 `docker run` 명령어 한 줄로 즉시 실행 가능한 서비스를 완성했습니다.
*   **기술적 성장**: 단순히 모델을 학습시키는 것을 넘어, **모델 서빙(Model Serving)**, **전처리 파이프라인**, **컨테이너 배포**로 이어지는 MLOps의 기초 사이클을 경험했습니다.
*   **사용자 중심 사고**: 개발자 관점이 아닌 사용자 관점에서 "직관적인 인터페이스"가 서비스의 가치를 결정한다는 점을 배웠습니다.

---
**Developed by flyingjoojak** | [GitHub Repository](https://github.com/joojak0616/mnist-streamlit)
