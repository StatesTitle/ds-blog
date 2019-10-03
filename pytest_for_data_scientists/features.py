import pandas as pd


def column_difference(df, col1, col2):
    """Subtract items in `col1` from items in `col2` elementwise (e.g. df[col1] - df[col2)]"""
    return df[col1] - df[col2]


def test_column_difference():  # (1)
    test_df = pd.DataFrame([(1, 2), (3, 4)], columns=["A", "B"])  # (2)
    test_df["A_minus_B"] = column_difference(test_df, col1="A", col2="B")  # (3)
    assert all(test_df["A_minus_B"] == pd.Series([-1, -1]))  # (4)
