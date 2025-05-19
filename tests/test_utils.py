import pandas as pd
import pytest
from viewer import read_file, clean_dataframe


@pytest.fixture
def sample_csv(tmp_path):
    file_path = tmp_path / "test.csv"
    file_path.write_text("name , age \n Alice , 30 \n Bob , 25 ")
    return file_path


def test_read_file_csv(sample_csv):
    df = read_file(sample_csv)
    assert df is not None
    assert df.shape == (2, 2)
    assert "name " in df.columns or "name" in df.columns


def test_clean_dataframe():
    raw_df = pd.DataFrame(
        {
            " name ": [" Alice ", " Bob ", None],
            " age ": [" 30", "25", None],
            "empty": [None, None, None],
        }
    )
    clean_df = clean_dataframe(raw_df)
    assert clean_df.shape == (2, 2)
    assert list(clean_df.columns) == ["name", "age"]
    assert clean_df.iloc[0]["name"] == "Alice"
