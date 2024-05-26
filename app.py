import os
import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf 

model = tf.keras.models.load_model('./cnn_model.keras')

def imgDetection(image):
    image.save('detect_img.png')
    image_path = 'detect_img.png'
    image_data = tf.io.read_file(image_path)
    image_data = tf.image.decode_image(image_data, channels=3)
    image_data = tf.image.resize(image_data, [128, 128])
    image_data = tf.cast(image_data, tf.float32) / 255.0

    pred = model.predict(tf.expand_dims(image_data, 0))[0]
    probs = tf.nn.softmax(pred).numpy()
    class_dist = {
            "Non_Demented": 3200,
            "Mild_Demented": 896,
            "Moderate_Demented": 64,
            "Very_Mild_Demented": 2240,
        }
    probs_dict = dict(zip(class_dist.keys(), probs))
    print(probs_dict)
    os.remove(image_path)
    return probs_dict

def main():
    st.title("Alzheimer's Disease MRI Image Detection")

    uploaded_file = st.file_uploader("Choose a file...", type=["jpg", "png", "jpeg", "webp"])  # jpg, jpeg, png

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        detection_results = imgDetection(image)
        st.write("Detected Results:")
        
        for label, confidence in detection_results.items():
            confidence_rounded = round(confidence * 100, 3)
            st.write(f"{label}: {confidence_rounded}%")
            st.progress(int(confidence * 100))

if __name__ == "__main__":
    main()
