import streamlit as st
import os
import requests
import joblib
from PIL import Image
import numpy as np
import numpy as np
from keras.preprocessing import image

url = "https://chatgpt-42.p.rapidapi.com/conversationgpt4"
def main():
    model = joblib.load('model_saved')
    st.title("DiscoverArt: Your Virtual Museum Guide")
    central_idea ="Empower Your Art Exploration: A Virtual Museum Guide utilizing image-to-text and question-answering technologies. Uncover the stories behind artworks and historical artifacts by uploading photos, receiving detailed information, and exploring their cultural contexts through interactive Q&A. Welcome to a seamless blend of art and technology!"

    st.markdown(central_idea, unsafe_allow_html=True)

   
    # Upload image
    uploaded_file = st.file_uploader("Choose an image:", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Save the uploaded image temporarily
        temp_image_path = "temp_image.jpg"  # You can use a different file name or extension
        save_uploaded_image(uploaded_file, temp_image_path)

        # Display the uploaded image
        st.image(temp_image_path, caption="Uploaded Image", use_column_width=False, width=200)
        # st.image()

 
        image_path = temp_image_path
        image1 = Image.open(image_path)


        test_image = image.load_img("temp_image.jpg", target_size = (64, 64))

        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        predictions = model.predict(test_image)

        predicted_class_index = np.argmax(predictions)



        print(f"Predicted class index: {predicted_class_index}")



    st1 = st.text_input("Ask a Question:", "")
    if st.button("Generate Answer"):
    # Perform any processing on the entered string here
        processed_result = process_string(st1)
        st.write("Processed result:", processed_result)
    

def process_string(st1):
    # Replace this with your actual processing logic
    # For example, converting the string to uppercase
    # return input_string.upper()
    st1=st1+"specific info only in short "

    payload = {
        "messages": [
            {
                "role": "user",
                "content": st1
        }
        ],
        "system_prompt": "",
        "temperature": 0.9,
        "top_k": 5,
        "top_p": 0.9,
        "max_tokens": 256,
        "web_access": False
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "f4c8516255mshfc51361ba078b2dp1e8cc5jsn052a8eeeb4e6",
        "X-RapidAPI-Host": "chatgpt-42.p.rapidapi.com"
    }
    print("Hello ")
    response = requests.post(url, json=payload, headers=headers)
    # y=next(iter(response.json()))
    y= response.json().get("result")
    return y

def save_uploaded_image(uploaded_file, save_path):
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

# Function to delete the temporary image
def delete_temporary_image(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

if __name__ == "__main__":
    main()