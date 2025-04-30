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
### 1. Prerequisites
- Install Docker: Get Docker
- Install kubectl: Get kubectl
- Install Kind: Get Kind
- Install Helm: Get Helm
### 2. Create Kind Cluster with Ingress Ports
```bash
kind delete cluster
kind create cluster --config kind-config.yaml
```
### 3. Install Nginx Ingress for Kind
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```
Wait for the ingress controller to be ready:
```bash
kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=180s
```
### 4. Install Prometheus & Grafana (Monitoring)
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace monitoring
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring
```
### 5. Build and Load Your Docker Image into Kind
```bash
docker build -t butterfly-classifier:latest .
kind load docker-image butterfly-classifier:latest
```
### 6. Deploy Your Application
```bash
kubectl apply -f deployment/deployment.yaml
kubectl apply -f deployment/service-cluster-ip.yaml
kubectl apply -f deployment/service-ingress.yaml
kubectl apply -f deployment/servicemonitor.yaml
kubectl apply -f deployment/hpa.yaml
```

### 7. Verify Everything is Running
```bash
kubectl get pods
kubectl get svc
kubectl get ingress
kubectl get hpa
```

## Testing
To test work of this repo:
```bash
curl -X POST -H "Content-Type: application/json" -d @tests/post_data.txt http://localhost/classify
```

To test the load:
```bash
ab -n 1000 -c 10 -p tests/post_data.txt -T "application/json" http://localhost/classify
```

## Monitoring
Port-forward Grafana:
```bash
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```
user: admin
password: prom-operator

Port-forward Prometheus:
```bash
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
```

