from keras.utils import img_to_array
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.models import Model
import cv2
from PIL import Image
import pickle
import numpy as np

# Ham tao model
def get_extract_model():
    vgg16_model = VGG16(weights="imagenet")
    extract_model = Model(inputs=vgg16_model.inputs, outputs=vgg16_model.get_layer("fc1").output)
    return extract_model

# Ham tien xu ly, chuyen doi hinh anh thanh tensor
def image_preprocess(img):
    img = img.resize((224, 224))
    img = img.convert("RGB")
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

def extract_vector(model, image_path):
    print("Loading...")
    img_tensor = image_preprocess(image_path)

    # Trich dac trung
    vector = model.predict(img_tensor)[0]
    # Chuan hoa vector = chia chia L2 norm (tu google search)
    vector = vector / np.linalg.norm(vector)
    return vector

def predict(search_image): 
    # Khoi tao model
    model = get_extract_model()

    # Trich dac trung anh search
    search_vector = extract_vector(model, search_image)

    # Load 4700 vector tu vectors.pkl ra bien
    vectors = pickle.load(open("Image_Search/vectors.pkl","rb"))
    paths = pickle.load(open("Image_Search/paths.pkl","rb"))

    # Tinh khoang cach tu search_vector den tat ca cac vector
    distance = np.linalg.norm(vectors - search_vector, axis=1) #là căn bậc hai của tổng bình phương các phần tử của ma trận (duyệt theo phần tử trong vector axis=1)
    # print(distance)
    # Sap xep va lay ra K vector co khoang cach ngan nhat
    K = 6
    ids = np.argsort(distance)[: K]
    print(ids)
    # Tao output
    # nearest_image = [(paths[id], distance[id]) for id in ids]
    nearest_image = [paths[id] for id in ids]
    return nearest_image
    
