import cv2
import numpy as np

def preprocess_image(image_data):
    """
    Canvas에서 받은 이미지 데이터를 모델 입력 형태(1, 1, 28, 28)로 전처리합니다.
    
    Args:
        image_data (numpy.ndarray): Canvas의 RGBA 이미지 데이터
        
    Returns:
        numpy.ndarray: 전처리된 이미지 (Batch size, Channels, Height, Width)
        numpy.ndarray: 시각화용 이미지 (28x28)
    """
    # 1. Alpha 채널만 사용하여 그레이스케일로 변환 (검은 배경에 흰 글씨라고 가정)
    # Canvas가 보통 흰 배경에 검은 글씨거나 그 반대일 수 있음.
    # streamlit-drawable-canvas는 보통 RGBA를 반환함.
    
    # 이미지 데이터가 없으면 None 반환
    if image_data is None:
        return None, None

    # numpy array로 변환 (이미 되어있을 수 있음)
    img = np.array(image_data).astype('uint8')
    
    # RGBA -> Grayscale
    # 보통 배경이 투명(0)이거나 흰색(255)일 수 있음.
    # 사용자가 검은색으로 그렸다면? -> 투명 배경에 검은 획
    # MNIST 모델은 검은 배경에 흰 글씨(0~255)를 기대함.
    
    # 캔버스 설정에 따라 다르지만, 보통 stroke_color="#FFFFFF" (흰색)으로 설정하고 background_color="#000000" (검은색)으로 하면 MNIST와 흡사.
    # 만약 투명 배경이라면 Alpha 채널을 활용.
    
    if img.shape[-1] == 4:
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
    else:
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 2. 28x28로 리사이즈
    img_resized = cv2.resize(img_gray, (28, 28), interpolation=cv2.INTER_AREA)
    
    # 3. 정규화 (0~1) 및 타입 변환 (float32)
    # MNIST 모델 입력은 Float32 [1, 1, 28, 28]
    img_normalized = img_resized.astype(np.float32) / 255.0
    
    # 4. 차원 확장
    img_input = np.expand_dims(img_normalized, axis=0) # (1, 28, 28)
    img_input = np.expand_dims(img_input, axis=0)      # (1, 1, 28, 28)
    
    return img_input, img_resized
