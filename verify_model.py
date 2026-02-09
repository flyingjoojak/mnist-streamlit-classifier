import sys
import os

# 현재 디렉토리를 경로에 추가하여 utils 패키지 인식 가능하게 함
sys.path.append(os.getcwd())

from utils.model_loader import download_model
import onnxruntime as ort

print("=== 모델 로드 테스트 시작 ===")

# Streamlit 의존성 없이 다운로드 테스트
try:
    if not os.path.exists("mnist-8.onnx"):
        print("모델 파일이 없습니다. 다운로드를 시도합니다...")
        import requests
        MODEL_URL = "https://github.com/onnx/models/raw/main/validated/vision/classification/mnist/model/mnist-8.onnx"
        response = requests.get(MODEL_URL)
        with open("mnist-8.onnx", "wb") as f:
            f.write(response.content)
        print("다운로드 완료!")
    else:
        print("모델 파일이 이미 존재합니다.")
        
    print("ONNX Runtime 세션 생성 시도...")
    session = ort.InferenceSession("mnist-8.onnx")
    print("성공! 입력 노드 이름:", session.get_inputs()[0].name)
    
except Exception as e:
    print(f"오류 발생: {e}")
    sys.exit(1)

print("=== 테스트 완료 ===")
