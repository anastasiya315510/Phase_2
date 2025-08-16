
# 🌍 Phase 2: Orchestration - Kubernetes Basics & Advanced

**Flask Hello World** is a lightweight, containerized web application built with Flask and served via Gunicorn. In Phase 2, we orchestrate this application using Kubernetes to deploy a scalable and highly available system.

---

## 🚀 Features

* **Minimal Flask App:** Basic route returning `Hello, World!`
* **Production-Ready:** Uses Gunicorn instead of Flask’s development server
* **Containerized & Kubernetes-Ready:** Easily deployable using Docker and Kubernetes
* **Scalable:** Horizontal Pod Autoscaling (HPA) included
* **Configurable:** Uses ConfigMaps and Secrets for environment management
* **Health-Monitored:** Liveness and Readiness Probes implemented
* **Automated Tasks:** CronJobs for periodic operations

---

## 🗂 Project Structure

```
Phase_2/
├── manifests/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
│   ├── cronjob.yaml
│   ├── configmap.yaml
│   └── secret.yaml
├── app.py
├── Dockerfile
├── requirements.txt
└── task.py              # CronJob task
```

---

## Full diagram

```
                   ┌───────────────────────┐
                   │    Deployment         │
                   │  flask-deployment     │
                   └─────────┬─────────────┘
                             │ manages
                             ▼
                ┌───────────────────────────┐
                │          Pods             │
                │flask-container(3 replicas)│
                │  ┌─────────────────────┐  │
                │  │ Liveness Probe      │  │
                │  │ /health             │  │
                │  └─────────────────────┘  │
                │  ┌─────────────────────┐  │
                │  │ Readiness Probe     │  │
                │  │ /ready              │  │
                │  └─────────────────────┘  │
                └─────────┬─────────────────┘
                          │ exposed via
                          ▼
                   ┌──────────────────┐
                   │    Service       │
                   │  flask-service   │
                   │  Type: NodePort  │
                   └─────────┬────────┘
                             │ monitored by
                             ▼
                     ┌───────────────┐
                     │ HPA Controller│
                     │ CPU Metrics   │
                     │ min: 2, max: 5│
                     └───────────────┘

           ┌───────────────────────────────────┐
           │            CronJobs               │
           │  Periodic tasks via task.py       │
           │  Pod runs → completes → exits     │
           └───────────────────────────────────┘

```

## 🧑‍💻 Prerequisites

* Docker
* Minikube or k3s (for local Kubernetes cluster)
* kubectl CLI
* Python 3.9+

---

## 🚀 Phase 2 Recap: Running Locally

### Locally

```bash
git clone https://github.com/anastasiya315510/Phase_2.git
cd Phase_2
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Visit: [http://localhost:8000](http://127.0.0.1:8000)

### With Docker Compose

```bash
docker compose build
docker compose up
docker compose down
```

### Manual Docker Commands

```bash
docker build -t flask-hello-world:latest .
docker run -d -p 8000:8000 --name flask-app flask-hello-world:latest
```

---

## 🧑‍💻 Phase 2: Kubernetes Deployment

### 1. Kubernetes Cluster Setup

```bash
minikube start \
  --cpus=2 \
  --memory=4096 \
  --disk-size=20g \
  --driver=docker \
  --profile=dev-cluster
minikube addons enable metrics-server --profile=dev-cluster
minikube addons enable dashboard --profile=dev-cluster
kubectl get nodes --context=dev-cluster
```

---

### 2. Deploy Application

```bash
docker push 315510/flask-hello-world:latest
kubectl apply -f manifests/pod.yaml --context=dev-cluster
kubectl get pods --context=dev-cluster
kubectl port-forward pod/flask-pod 8000:8000 --context=dev-cluster
```

---

### 3. Deployment, ReplicaSet & Service

```bash
kubectl apply -f manifests/deployment.yaml --context=dev-cluster
kubectl apply -f manifests/service.yaml --context=dev-cluster
kubectl get service flask-service --context=dev-cluster
minikube service flask-service --url --profile=dev-cluster
```

---

### 4. Horizontal Pod Autoscaling (HPA)

```bash
kubectl apply -f manifests/hpa.yaml --context=dev-cluster
kubectl get hpa --context=dev-cluster
```

**HPA Diagram:**

```
          ┌───────────────┐
          │ Deployment    │
          │ (flask-app)   │
          └─────┬─────────┘
                │ manages
                ▼
          ┌───────────────┐
          │Pods (replicas)│
          └─────┬─────────┘
                │ CPU metrics
                ▼
          ┌───────────────┐
          │HPA Controller │
          └─────┬─────────┘
                │ scales pods
                ▼
          ┌───────────────┐
          │ Updated Pods  │
          └───────────────┘
```

---

### 5. ConfigMaps and Secrets

```bash
kubectl apply -f manifests/configmap.yaml --context=dev-cluster
kubectl apply -f manifests/secret.yaml --context=dev-cluster
```

---

### 6. CronJobs

```bash
kubectl apply -f manifests/cronjob.yaml --context=dev-cluster
kubectl get cronjobs --context=dev-cluster
kubectl get jobs --context=dev-cluster
kubectl logs <cronjob-pod-name> -c flask-cron --context=dev-cluster
```

---

### 7. Liveness and Readiness Probes

Add to `deployment.yaml`:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 15
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3
```

Update Deployment:

```bash
kubectl apply -f manifests/deployment.yaml --context=dev-cluster
```

---


