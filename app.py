import streamlit as st
import numpy as np
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from utils.model_loader import load_model
from utils.preprocessing import preprocess_image

# 페이지 설정
st.set_page_config(
    page_title="MNIST 숫자 분류기",
    page_icon="🔢",
    layout="wide"
)

# 세션 상태 초기화 (이미지 저장소)
if 'history' not in st.session_state:
    st.session_state['history'] = []

def main():
    st.title("🖌️ 손글씨 숫자 인식기 (MNIST)")
    st.markdown("왼쪽 캔버스에 0부터 9까지의 숫자를 그려보세요. 인공지능이 어떤 숫자인지 맞춰봅니다.")
    
    # 모델 로드
    session = load_model()
    if session is None:
        st.stop()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. 숫자 그리기")
        # 캔버스 설정
        canvas_result = st_canvas(
            fill_color="rgba(0, 0, 0, 0)",  # 투명 채우기
            stroke_width=20,                # 붓 두께
            stroke_color="#FFFFFF",         # 흰색 붓
            background_color="#000000",     # 검은색 배경
            height=280,
            width=280,
            drawing_mode="freedraw",
            key="canvas",
        )
        
        st.info("숫자를 큼지막하게 중앙에 그려주세요!")

    inference_result = None
    processed_img_display = None

    with col2:
        st.subheader("2. 분석 결과")
        
        if canvas_result.image_data is not None:
            # 전처리
            input_tensor, processed_img_display = preprocess_image(canvas_result.image_data)
            
            # 아무것도 그리지 않았을 때 (검은색만 있을 때) 처리
            # np.sum(processed_img_display) == 0 이면 빈 캔버스
            if processed_img_display is not None and np.sum(processed_img_display) > 0:
                
                # 전처리된 이미지 시각화
                st.image(processed_img_display, caption="전처리된 이미지 (28x28)", width=140)
                
                # 추론
                input_name = session.get_inputs()[0].name
                output_name = session.get_outputs()[0].name
                result = session.run([output_name], {input_name: input_tensor})
                
                # 결과 처리 (logits -> softmax or just visualization)
                # MNIST ONNX 모델 출력은 보통 Logits (1x10)
                logits = result[0][0]
                
                # Softmax 적용 (확률 변환)
                exp_logits = np.exp(logits - np.max(logits))
                probs = exp_logits / exp_logits.sum()
                
                inference_result = probs
                predicted_label = np.argmax(probs)
                confidence = probs[predicted_label]
                
                st.markdown(f"### 예측 결과: **:blue[{predicted_label}]**")
                st.progress(float(confidence))
                st.caption(f"확률: {confidence:.2%}")
                
                # 막대 차트
                chart_data = pd.DataFrame(
                    probs,
                    columns=["확률"],
                    index=[str(i) for i in range(10)]
                )
                st.bar_chart(chart_data)

            else:
                st.warning("캔버스에 숫자를 그려주세요.")

    # 저장 기능
    st.divider()
    st.subheader("📂 이미지 저장소")
    
    if st.button("현재 결과 저장하기"):
        if inference_result is not None and processed_img_display is not None:
            # 히스토리에 저장
            st.session_state['history'].append({
                "image": processed_img_display,
                "prediction": np.argmax(inference_result),
                "confidence": np.max(inference_result)
            })
            st.success("저장되었습니다!")
        else:
            st.error("저장할 결과가 없습니다.")

    # 저장된 이미지 갤러리
    if st.session_state['history']:
        # 최신 순으로 보여주기
        hist_cols = st.columns(min(len(st.session_state['history']), 5))
        
        # 최근 5개만 표시한다고 가정 (혹은 그리드 처리)
        recent_history = st.session_state['history'][::-1]
        
        for idx, item in enumerate(recent_history):
            if idx < 5: # 5개까지만 표시
                with hist_cols[idx]:
                    st.image(item['image'], width=100)
                    st.markdown(f"**{item['prediction']}** ({item['confidence']:.1%})")

if __name__ == "__main__":
    main()
