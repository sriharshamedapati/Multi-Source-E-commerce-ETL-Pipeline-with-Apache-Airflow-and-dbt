FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
# Install requirements + uvicorn for the server
RUN pip install --no-cache-dir -r requirements.txt uvicorn fastapi
COPY main.py .
EXPOSE 8000
# The correct way to start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]