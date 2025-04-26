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
kind create cluster --config=kind/kind-config.yaml
```
2. Build an image from Dockerfile
```bash
docker build -t butterfly-classifier .
```
3. Load the image to kind cluster
```bash
kind load docker-image butterfly-classifier:latest
```
4. Start Nginx Ingress Controller
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```
5. Edit `C:\Windows\System32\drivers\etc\hosts` and add this line:
```bash
127.0.0.1 api.butterfly.me
```
6. Start deployment and service
```bash
kubectl apply -f deployment/deployment.yaml
kubectl apply -f deployment/service-cluster-ip.yaml
kubectl apply -f deployment/service-ingress.yaml
```
7. Open `client.html` with browser.