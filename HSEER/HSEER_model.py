import torch
import timm
import torch.nn as nn
from torchvision.transforms import transforms
from PIL import Image
import numpy as np
import cv2


def detect_face(frame_path, face_recongizer):
    frame = cv2.imread(frame_path)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    bounding_boxes, probs = face_recongizer.detect(frame, landmarks=False)
    if probs is None:
        return False
    else:
        bounding_boxes = bounding_boxes[probs > 0.9]
        for bbox in bounding_boxes:
            box = bbox.astype(int)
            x1, y1, x2, y2 = box[:4]

            face_image = frame[y1:y2, x1:x2, :]
        return face_image


class HSEER:
    def __init__(self, model_path: str, device='cpu'):
        self.device = device

        self.idx2class = {0: 'unhappy', 1: 'happy', 2: 'neutral'}
        img_size = 224
        self.transforms = transforms.Compose([
            transforms.Resize([img_size, img_size]),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        if 'b0' in model_path:
            classifier_path = 'HSEER/models/classfiers/enetb0_classifier.pt'
        else:
            classifier_path = 'models/classfiers/enetb2_classifier.pt'

        if self.device == 'cpu':
            model = torch.load(model_path, map_location=self.device)
            model_last_layer_input = model.classifier.in_features
            self.classifier = nn.Linear(model_last_layer_input, len(self.idx2class.keys()))
            self.classifier.load_state_dict(torch.load(classifier_path, map_location=self.device))
        else:
            model = torch.load(model_path)
            model_last_layer_input = model.classifier.in_features
            self.classifier = nn.Linear(model_last_layer_input, len(self.idx2class.keys()))
            self.classifier.load_state_dict(torch.load(classifier_path))

        model.classifier = nn.Identity()
        model = model.to(device)
        self.model = model.eval()

    def extract_features(self, image):
        image_tensor = self.transforms(Image.fromarray(image))
        image_tensor.unsqueeze(0)
        image_tensor = image_tensor.to(self.device)
        image_tensor = image_tensor.unsqueeze(0)
        features = self.model(image_tensor)

        return features

    def predict_emotion(self, image):
        features = self.extract_features(image)
        classifier_output = self.classifier(features)
        predicted_emotion = torch.argmax(classifier_output, 1)

        return self.idx2class[predicted_emotion.item()]
    
