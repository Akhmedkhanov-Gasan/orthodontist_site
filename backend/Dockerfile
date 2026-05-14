FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        pkg-config \
        libcairo2-dev \
        libgirepository1.0-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "orthodontist_site.wsgi"]