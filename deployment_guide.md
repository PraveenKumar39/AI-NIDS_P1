# AI-NIDS Deployment Guide

This guide covers how to deploy the AI-NIDS to **Streamlit Cloud** (Easiest) and **Docker** (Best for production).

---

## ☁️ Option 1: Streamlit Cloud (Recommended for Demos)
Streamlit Cloud hosts your dashboard for free directly from GitHub.

### 1. Push Code to GitHub
1.  Initialize Git (if not done):
    ```bash
    git init
    git add .
    git commit -m "Final release of AI-NIDS"
    ```
2.  Create a new repository on [GitHub.com](https://github.com/new).
3.  Link and push:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/AI-NIDS.git
    git branch -M main
    git push -u origin main
    ```

### 2. Deploy on Streamlit
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Log in with GitHub.
3.  Click **"New app"**.
4.  Select your repository (`AI-NIDS`).
5.  **Main file path**: `app.py`
6.  Click **"Deploy!"**.

*Note: Streamlit Cloud will automatically install dependencies from `requirements.txt`.*

---

## 🐳 Option 2: Docker (Production API)
Run the API as a containerized microservice.

### 1. Build the Image
```bash
docker build -t ai-nids .
```

### 2. Run the Container
```bash
docker run -p 8000:8000 ai-nids
```

### 3. Verify
-   API Health: `http://localhost:8000/health`
-   Swagger UI: `http://localhost:8000/docs`

---

## 🔧 Troubleshooting
-   **CSV Not Found**: If Streamlit can't find `data/`, ensure `data/` is included in your git commit (check `.gitignore`).
-   **Model Error**: Ensure `models/rf_model.pkl` is committed and pushed.
