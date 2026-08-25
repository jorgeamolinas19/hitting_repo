# Deployment Guide

## Streamlit Cloud Deployment

### Prerequisites
- GitHub account with repository containing the app
- Streamlit account

### Steps

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Click "New app"
4. Select your repository and branch
5. Set the main file path to `app.py`
6. Click "Deploy"

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

### Build and Run
```bash
docker build -t hitting-analytics .
docker run -p 8501:8501 hitting-analytics
```

## Environment Variables

Set any required environment variables before deployment:
```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
```
