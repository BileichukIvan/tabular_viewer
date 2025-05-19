FROM python:3.11-slim

# Installing system dependencies
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt1-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Copy files
COPY . /app

# Installing Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Відкриття порту
EXPOSE 8501

# Streamlit launch command
CMD ["streamlit", "run", "viewer.py", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
