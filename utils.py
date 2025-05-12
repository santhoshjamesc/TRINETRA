'''
Helper functions for face recognition
'''
import numpy as np
import random
import os
import cv2
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Conv2D, MaxPooling2D
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.backend import sum as K_sum, square as K_square, sqrt as K_sqrt, maximum as K_maximum, epsilon as K_epsilon, mean as K_mean, equal as K_equal, cast as K_cast

# Euclidean Distance Function
def euclidean_distance(vectors):
    vector1, vector2 = vectors
    sum_square = K_sum(K_square(vector1 - vector2), axis=1, keepdims=True)
    return K_sqrt(K_maximum(sum_square, K_epsilon()))

# Contrastive Loss Function
def contrastive_loss(Y_true, D):
    margin = 1
    return K_mean(Y_true * K_square(D) + (1 - Y_true) * K_maximum((margin - D), 0))

# Accuracy Metric
def accuracy(y_true, y_pred):
    return K_mean(K_equal(y_true, K_cast(y_pred < 0.5, y_true.dtype)))

# Create Pairs for Siamese Network
def create_pairs(X, Y, num_classes):
    X = np.array(X)  # Ensure X is a NumPy array
    Y = np.array(Y)  # Ensure Y is a NumPy array
    pairs, labels = [], []
    class_idx = [np.where(Y == i)[0] for i in range(num_classes)]
    min_images = min(len(class_idx[i]) for i in range(num_classes)) - 1

    for c in range(num_classes):
        for n in range(min_images):
            # Positive pair
            pairs.append((X[class_idx[c][n]], X[class_idx[c][n + 1]]))
            labels.append(1)

            # Negative pair
            neg_list = list(range(num_classes))
            neg_list.remove(c)
            neg_c = random.choice(neg_list)
            pairs.append((X[class_idx[c][n]], X[class_idx[neg_c][n]]))
            labels.append(0)

    return np.array(pairs), np.array(labels)

# Create Shared Convolutional Network
def create_shared_network(input_shape):
    model = Sequential(name='Shared_Conv_Network')
    model.add(Conv2D(64, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D())
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Flatten())
    model.add(Dense(128, activation='sigmoid'))
    return model

# Load and Process Dataset
def get_data(dir, img_size=(100, 100)):
    X_train, Y_train = [], []
    X_test, Y_test = [], []

    subfolders = sorted([file.path for file in os.scandir(dir) if file.is_dir()])

    for idx, folder in enumerate(subfolders):
        for file in sorted(os.listdir(folder)):
            img_path = os.path.join(folder, file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Read as grayscale
            if img is None:
                print(f"Warning: Unable to load {img_path}")
                continue
            img = cv2.resize(img, img_size)  # Resize to fixed size
            img = img.astype('float32') / 255.0  # Normalize
            img = np.expand_dims(img, axis=-1)  # Add channel dimension

            if idx < 35:
                X_train.append(img)
                Y_train.append(idx)
            else:
                X_test.append(img)
                Y_test.append(idx - 35)

    X_train = np.array(X_train, dtype=np.float32)
    X_test = np.array(X_test, dtype=np.float32)
    Y_train = np.array(Y_train, dtype=np.int32)
    Y_test = np.array(Y_test, dtype=np.int32)

    return (X_train, Y_train), (X_test, Y_test)

# Write Text on Video Frame
def write_on_frame(frame, text, text_x, text_y):
    (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=2)
    box_coords = ((text_x, text_y), (text_x + text_width + 20, text_y - text_height - 20))
    cv2.rectangle(frame, box_coords[0], box_coords[1], (255, 255, 255), cv2.FILLED)
    cv2.putText(frame, text, (text_x, text_y - 10), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0), thickness=2)
    return frame
