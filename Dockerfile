FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV AEGISCORP_PORT=8000
ENV AEGISCORP_HOST=0.0.0.0

CMD ["python", "-m", "aegiscorp.cli.main", "serve", "--host", "0.0.0.0", "--port", "8000"]
