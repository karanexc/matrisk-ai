FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY packages.txt .

RUN apt-get update && \
    xargs -a packages.txt apt-get install -y && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/dashboard/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]