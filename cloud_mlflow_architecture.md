# Cloud Infrastructure & MLflow Central Architecture

## 1. Local vs. Central MLflow Tracking
* **Local MLflow**: Runs only on your machine (`127.0.0.1:5000`). Metrics and models are stored locally and lost if the workspace is reset.
* **Central Tracking Server**: A live web application (FastAPI/Python engine) running continuously on a cloud server (e.g., Azure VM, AWS EC2, or Docker container) inside a corporate network.

---

## 2. Dual-Storage Backend Architecture
Production MLflow uses a split-tier storage design:
1. **Backend Store (Metadata)**:
   * **Stores**: Run IDs, metrics (RMSE), hyperparameters, tags, timestamps.
   * **Technology**: Relational SQL Database (PostgreSQL, MySQL).
2. **Artifact Store (Heavy Binary Files)**:
   * **Stores**: Saved model binaries (`.pkl`, `.json`), preprocessors, plots, dataset artifacts.
   * **Technology**: Cloud Object Storage (Azure Blob Storage, Amazon S3, Google Cloud Storage).

---

## 3. How MLflow Acts as a Proxy
When your script calls `mlflow.set_tracking_uri("http://mlflow.company.com")`:
1. **HTTP Transfer**: Your Python script sends metrics and model files via HTTP to the MLflow Central Server.
2. **Database Logging**: MLflow writes parameters and metrics into the backend PostgreSQL database.
3. **Artifact Upload (Proxy)**: MLflow uploads heavy model files directly to Azure Blob / S3 on your behalf—meaning client scripts don't need direct cloud database credentials.
4. **Artifact Downloading**: Functions like `download_artifacts()` fetch logged artifacts for a specific `run_id` to local storage on any machine for inference.

---

## 4. Corporate Cloud Networking Basics
* **Private IP Address**: Internal IP addresses (e.g., `10.0.1.45`) assigned within an Azure Virtual Network (VNet) or AWS VPC. Accessible only from connected cloud resources or employees using a corporate VPN.
* **Internal DNS Domain**: A friendly alias (e.g., `http://mlflow.internal.company.com`) mapped to the server's private IP.
