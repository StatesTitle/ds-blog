import pandas as pd
import pytest


def column_difference(df, col1, col2):
    """Subtract items in `col1` from items in `col2` elementwise (e.g. df[col1] - df[col2)]"""
    return df[col1] - df[col2]


def test_column_difference():
    # test common cases
    test_df = pd.DataFrame([(1, 2), (3, 4)], columns=["A", "B"])
    test_df["A_minus_B"] = column_difference(test_df, col1="A", col2="B")
    assert all(test_df["A_minus_B"] == pd.Series([-1, -1]))
    test_df = pd.DataFrame([(5, 3), (10, 14), (0, -8)], columns=["A", "B"])
    test_df["A_minus_B"] = column_difference(test_df, col1="A", col2="B")
    assert all(test_df["A_minus_B"] == pd.Series([2, -4, 8]))
    # Include a third column
    test_df = pd.DataFrame([(1, 2, 100), (3, 4, 200)], columns=["A", "B", "C"])
    test_df["A_minus_B"] = column_difference(test_df, col1="A", col2="B")
    assert all(test_df["A_minus_B"] == pd.Series([-1, -1]))
    # Tets column of zeros
    test_df = pd.DataFrame([(1, 0), (3, 0)], columns=["A", "B"])
    test_df["A_minus_B"] = column_difference(test_df, col1="A", col2="B")
    assert all(test_df["A_minus_B"] == pd.Series([1, 3]))
    # Test empty dataframe
    test_df = pd.DataFrame(columns=["A", "B"])
    test_df["A_minus_B"] = column_difference(test_df, col1="A", col2="B")
    assert all(test_df["A_minus_B"] == pd.Series([]))


test_columns_difference_params = [  # (1)
    # test common cases
    ([(1, 2), (3, 4)], ["A", "B"], [-1, -1]),
    ([(5, 3), (10, 14), (0, -8)], ["A", "B"], [2, -4, 8]),
    # Include a third column
    ([(1, 2, 100), (3, 4, 200)], ["A", "B", "C"], [-1, -1]),
    # Tets column of zeros
    ([(1, 0), (3, 0)], ["A", "B"], [1, 3]),
    # Test empty dataframe
    ([], ["A", "B"], []),
]


@pytest.mark.parametrize(
    "test_data, columns, expected_output", test_columns_difference_params  # (2)
)
def test_column_difference_with_parametrize(test_data, columns, expected_output):  # (3)
    test_df = pd.DataFrame(test_data, columns=columns)
    expected_series = pd.Series(expected_output)
    test_df["A_minus_B"] = column_difference(test_df, col1="A", col2="B")
    assert all(test_df["A_minus_B"] == expected_series)  # (4)
