import os
import requests
import onnxruntime as ort
import streamlit as st

MODEL_URL = "https://github.com/onnx/models/raw/main/validated/vision/classification/mnist/model/mnist-8.onnx"
MODEL_PATH = "mnist-8.onnx"

@st.cache_resource
def load_model():
    """
    ONNX 모델을 로드하고 세션을 반환합니다.
    모델 파일이 없으면 다운로드합니다.
    """
    if not os.path.exists(MODEL_PATH):
        try:
            download_model()
        except Exception as e:
            st.error(f"모델 다운로드 중 오류가 발생했습니다: {e}")
            return None

    try:
        session = ort.InferenceSession(MODEL_PATH)
        return session
    except Exception as e:
        st.error(f"모델 로딩 중 오류가 발생했습니다: {e}")
        return None

def download_model():
    """
    GitHub에서 MNIST ONNX 모델을 다운로드합니다.
    """
    with st.spinner("모델을 다운로드하는 중입니다..."):
        response = requests.get(MODEL_URL)
        response.raise_for_status()
        with open(MODEL_PATH, "wb") as f:
            f.write(response.content)
    st.success("모델 다운로드 완료!")
