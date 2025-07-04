# 📊 Table Data Viewer

A Streamlit web app for viewing tabular data files in various formats including CSV, Excel, SAS, and XPT.  
Supports automatic delimiter detection for CSV files and cleans data for better presentation.

# Features

- Supports CSV, XLSX, SAS7BDAT, and XPT file formats  
- Auto-detects CSV delimiters (comma, semicolon, or dollar sign)  
- Cleans data by trimming whitespace and removing empty rows and columns  
- Interactive file selection from the `data/` directory  
- Responsive UI with Streamlit  

# Getting Started

## Prerequisites

- Python 3.8+  
- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) (optional, for containerized setup)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/tabular_viewer.git
    cd tabular_viewer
    ```

2. Install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Running the app

### Locally
```bash
    streamlit run viewer.py
```

#### Tests. You can run tests with:
```bash
  pytest tests/
```

### Run with Docker:

```bash
   docker compose up --build 
```
Open your browser at **http://localhost:8501**

### For running test inside docker container:
```bash
   docker exec -it streamlit-viewer pytest tests/ 
```