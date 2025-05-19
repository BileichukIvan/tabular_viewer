import streamlit as st
import pandas as pd
import pyreadstat
from pathlib import Path
from typing import Optional, Tuple, List

st.set_page_config(page_title="📊 Table Data Viewer", layout="wide")
st.title("📊 Table Data Viewer")

DATA_DIR = Path("data")


def detect_csv_delimiter(sample: str) -> str:
    """Automatically detects the CSV delimiter from a text sample."""
    if "," in sample:
        return ","
    if "$" in sample:
        return "$"
    return ";"


def read_file(path: Path) -> Optional[pd.DataFrame] or Optional[str]:
    """
    Reads tabular data from a supported file.

    Supported formats: CSV, XLSX, SAS7BDAT, XPT.

    Returns a tuple (DataFrame or None, error message or None).
    """
    ext = path.suffix.lower()
    try:
        if ext == ".csv":
            with open(path, "r", encoding="utf-8") as f:
                sample = f.read(1024)
            delimiter = detect_csv_delimiter(sample)
            df = pd.read_csv(path, delimiter=delimiter)
            return df
        elif ext == ".xlsx":
            df = pd.read_excel(path)
            return df
        elif ext == ".sas7bdat":
            df, _ = pyreadstat.read_sas7bdat(path)
            return df
        elif ext == ".xpt":
            df, _ = pyreadstat.read_xport(path)
            return df
        else:
            return f"Unsupported file extension: {ext}"
    except FileNotFoundError:
            return f"File not found: {path.name}"
    except pd.errors.EmptyDataError:
        return f"File is empty or has no data: {path.name}"
    except pd.errors.ParserError:
        return f"Parsing error while reading file: {path.name}"
    except (OSError, IOError) as e:
        return f"I/O error while reading file {path.name}: {e}"
    except Exception as e:
        return f"Unexpected error while reading {path.name}: {e}"


@st.cache_data(show_spinner="Cleaning data...")
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans a DataFrame by removing empty rows and columns,
    and trimming whitespace from text data.
    """
    df = df.copy()
    df.columns = df.columns.str.strip()
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df.dropna(axis=1, how="all", inplace=True)
    df.dropna(axis=0, how="all", inplace=True)
    return df


def get_supported_files(data_dir: Path) -> List[Path]:
    """Collects a list of supported files in the given data directory."""
    files = list(data_dir.glob("**/*"))
    return [
        f for f in files if f.suffix.lower() in [".csv", ".xlsx", ".sas7bdat", ".xpt"]
    ]


def main():
    table_files = get_supported_files(DATA_DIR)

    if not table_files:
        st.error("📂 No supported tabular files found in the 'data/' directory.")
        return

    selected_name = st.selectbox(
        "📁 Select a file to view", [f.name for f in table_files]
    )
    selected_file = next(f for f in table_files if f.name == selected_name)

    df = read_file(selected_file)
    df = clean_dataframe(df)

    if df.empty:
        st.warning(f"⚠️ File **{selected_file.name}** contains no data.")
        return

    st.success(f"✅ Successfully loaded: **{selected_file.name}**")
    st.markdown(f"📐 **Shape:** `{df.shape[0]} rows × {df.shape[1]} columns`")
    st.markdown(f"🧾 **Columns:** {', '.join(df.columns)}")

    st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    main()
