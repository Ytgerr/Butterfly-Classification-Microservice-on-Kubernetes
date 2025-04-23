# DNP_project_17

# Butterfly Species Classifier

## Description
A web-based application that uses machine learning to classify butterfly species from uploaded images. The system provides real-time classification with confidence scores and supports drag-and-drop or click-to-upload functionality.

## Architecture
- Frontend: HTML/CSS/JavaScript web interface
- Backend: Containerized classification service
- Deployment: Kubernetes cluster using Kind

## Features
- Drag-and-drop image upload
- Real-time image classification
- Confidence score visualization
- Top 3 prediction results
- Responsive design
- Visual feedback during classification

## Setup
1. Install Kind and create a cluster:
```bash
# by using chocolate
choco install kind
```
2. Build an image from Dockerfile
```bash
docker build -t butterfly-classifier .
```
3. Load the image to kind cluster
```bash
kind load docker-image butterfly-classifier:latest \
    --config=kind/kind-config.yaml
```
4. Start deployment and service
```bash
kubectl apply -f deployment/deployment.yaml
kubectl apply -f deployment/service.yaml
```
5. Open `client.html` with browser.