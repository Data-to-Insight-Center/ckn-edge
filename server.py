# server.py
from flask import Flask, request, jsonify
import time
import torch
from torchvision import models, transforms
from PIL import Image

app = Flask(__name__)

# Load ResNet model
model = models.resnet152(pretrained=True)
model.eval()

# Load ImageNet class labels
with open("imagenet_classes.txt", "r") as f:
    labels = [line.strip() for line in f]

# Preprocessing pipeline
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return "ResNet server is running."

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    """Accepts an image and returns the top prediction along with compute time"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Measure total compute time (preprocessing + inference)
    start_time = time.time()
    try:
        image = Image.open(file.stream).convert('RGB')
    except Exception as e:
        return jsonify({'error': f'Invalid image: {str(e)}'}), 400

    input_tensor = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        top_prob, top_catid = torch.topk(probabilities, 1)

    compute_time = time.time() - start_time

    return jsonify({
        'label': labels[top_catid.item()],
        'probability': top_prob.item(),
        'compute_time': compute_time
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
