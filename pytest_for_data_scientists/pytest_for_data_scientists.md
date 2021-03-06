# pytest for Data Scientists
Creating automated tests for software is second nature to great software engineers, and it’s a habit that data scientists should mirror. By thoroughly testing code used to develop a model, data scientists can increase model robustness and, as a result, create obsessed customers that stick to our product due to its reliability

Most tutorials and books on creating automated software tests are written for software engineers. Although there is a ton of useful information in these resources, I find that the examples are often hard to adapt to the problems we face as data scientists. As a result, I’ve found that there is much less focus on writing well tested software among data scientists. This is a shame because writing tests is key to creating maintainable software and reliable models that are easy to monitor, something that should be a top priority of every data scientist.

With that in mind, this post provides an introduction to a popular testing framework, pytest, with an example that will resonate with data scientists. We’ll explore pytest’s intuitive approach to testing through a motivating example for testing data science code. We’ll discuss a few ways of structuring a project to support testing. We’ll close by introducing pytest’s `parametrize` decorator, an advanced feature that enables writing simple tests for data-intensive code.

Before we get into the details of how to write tests in pytest, let’s talk a little more about the deeper reasons why I think writing tests is so important for data scientists.
## Why tests ensure greater model reliability
As I mentioned before, writing tests is key to writing maintainable software. This is particularly important for data science which follows an iterative research and development process that rotates through the steps of data cleaning, data analysis, feature engineering, and model development. Each time through this rotation builds on work that was done in a previous iteration - modifying, for example, code that’s used to generate a feature. How can we be confident that the changes we make don’t unintentionally affect other steps in the pipeline?

The answer is testing. When we’ve written a test that verifies that our feature generation code is correct, we can be confident that changes to the code are not changing the behavior of the feature in an unintended way. Often, we will make changes that break a test. This is okay! A test simply captures how a piece of code behaves at a certain time and the behavior of code can change! When this happens, we just need to understand why the behavior of the code changed and update the test accordingly. 

With this in mind, let’s take a look at how we can start testing our data science code with pytest!
## Prerequisites
Example code in this post is available in our [`ds-blog`](https://github.com/StatesTitle/ds-blog/) GitHub repo in a directory named [`pytest_for_data_scientists`](https://github.com/StatesTitle/ds-blog/pytest_for_data_scientists). This directory contains a ["requirements.txt"](https://github.com/StatesTitle/ds-blog/pytest_for_data_scientists/requirements.txt) that specifies required dependencies. See the [`README.md`](https://github.com/StatesTitle/ds-blog/pytest_for_data_scientists/README.md) file for more info.
## Developing tests in pytest
Before we can write a test, we need something to test! Suppose we need to create a new (simple) feature that is the difference of two columns in a dataframe. A common way of implementing this feature is to write a function that looks something like this:
```python
def column_difference(df, col1, col2):
    """Subtract items in `col1` from items in `col2` elementwise (e.g. df[col1] - df[col2)]"""
    return df[col1] - df[col2]
```
This allows us to compute the difference of two columns for any Pandas dataframe that we pass in. Calling the function looks like this:
```python
df["A_minus_B"] = column_difference(df, "A", "B")
```
In order to test this function, we need to define some input data, call the function on the input, and compare the returned output to the output that we expect. Here are those steps, written in a test function that we can run with pytest:
```python
def test_column_difference():  # (1)
    test_df = pd.DataFrame([(1, 2), (3, 4)], columns=["A", "B"])  # (2)
    test_df["A_minus_B"] = column_difference(test_df, col1="A", col2="B")  # (3)
    assert all(test_df["A_minus_B"] == pd.Series([-1, -1]))  # (4)
```
The following explains each line in the function above:

1. pytest searches for and runs functions that begin or end with the word `test`
2. We create a Pandas DataFrame that we will use as input to test our function
3. We call the function on the test DataFrame input
4. The condition in the `assert` statement causes the test to pass or fail depending on whether the statement is `True` or `False`

How do we run the test? There are a few options, but one option that fits data science development workflows is to run tests in a [Jupyter](https://jupyter.org/) notebook using the [`pip`](https://github.com/pypa/pip) installable module [`ipytest`](https://github.com/chmp/ipytest/). Here is an example of what that looks like for the test function we developed:

![Running the test in a notebook using ipytest](resources/run_test_with_ipytest2.png)

1. Configuration steps for `ipytest`, described [here](https://github.com/chmp/ipytest#usage)
2. We define our test function the same way as before
3. Command line arguments can be passed into `ipytest.run` as a string

There are a couple advantages to utilizing `pytest` when developing test functions in a Jupyter notebook. One advantage is that when the test fails, pytest provides a detailed diff that allows us to precisely pinpoint why the test failed. This is shown in the following:

![Running a failing test in a notebook shows a diff](resources/run_failing_test_with_ipytest.png)

1. We’ve changed the expected output of the test so that the test fails
2. The diff provided by `pytest` allows us to pinpoint exactly where the test failed

Another advantage of utilizing `pytest` in a Jupyter notebook is that it allows us to easily transition from a notebook to tests stored in a “.py” file once our project grows beyond the scope of a single Jupyter notebook. We'll touch more on this shortly.

One thing to be careful about with `ipytest` is renaming test functions during development. When a test function is defined and then subsequently renamed, the first definition still exists in the runtime of the notebook and will be called when `ipytest.run` is invoked. This can cause confusing behavior where modifying test code doesn’t seem to make any difference when running the tests.

Now, time to talk about every data scientist's favorite topic...
## Moving beyond a notebook
Once the project grows beyond the scope of a single notebook, we may want to move our feature creation function and the corresponding test code to a “.py” file.  When we do this, we can use the command line tool `py.test` that is installed along with `pytest` to run our test functions. For example, I’ve defined both our `column_difference` function and its corresponding test function in a file called “features.py”. Here is what calling `py.test` on that file looks like:
```bash
py.test -svvv ./features.py
```
This results in the following:

![Running the test with the py.test command line tool](resources/run_test_with_pytest.png)

Eventually, we may want to move our test code into a separate file. If we include “test” in the name of the file, just as we included “test” in the test function name, the `py.test` command line tool can automatically detect and run the test code in those files. More information about how test discovery works is available in the pytest [documentation](https://doc.pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery).
## Parametrizing data-intensive tests
So far, we’ve only provided one dataframe as input to our test function. We probably want to add a few more dataframes as separate test cases to ensure that our function works for a variety of input. One way to achieve that is to extend the test function with additional data and call the test function again:
```python
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
```
This works but it’s hard to tell that all we are doing is testing the same function over-and-over again with different input. Adding a comment to describe this would be an improvement but, since we are utilizing pytest, there is another way to write this test that makes the test code simple to understand. Specifically, the [`parametrize`](https://docs.pytest.org/en/latest/parametrize.html#pytest-mark-parametrize-parametrizing-test-functions) decorator allows us to separate the test data from the logic of the test function.

Here is the same example as above, using `parametrize`:
```python
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
```

1. We can define our test data examples upfront in a list with each item in the list representing a separate test case
2. The `parametrize` decorator takes two arguments: a comma separated string of the input arguments for the test function and the corresponding test data
3. The arguments in the function definition of the test must match the comma separated string of the input arguments passed into the decorator
4. Using `parametrize` makes the test code much easier to read

When we run a test function decorated with parametrize, each item in the list that defines the test parameters is run as a separate test input. Pytest shows whether each test passes or fails separately. An example of running the `py.test` command line tool on the `parametrize`d test function is shown below:

![Running a parametrized test provides output for each test input](resources/run_parametrized_test_with_pytest.png)

If one the the test inputs from the list causes the test to fail, we will see a diff for the failure just as before.

## Wrapping up
We’ve covered what a test looks like in `pytest`, how to run `pytest` tests in a notebook, and how to utilize the `parametrize` decorator to simplify data-intensive tests.

If you want to learn more about testing with `pytest`, the `pytest` [documentation](https://doc.pytest.org/en/latest/) is a great place to start! For those who want to dive a little deeper, the book ["Python testing with pytest"](https://pragprog.com/book/bopytest/python-testing-with-pytest) by Brian Okken is frequently recommended. For more tips about writing maintainable software, I recommend ["Working effectively with legacy code"](https://dl.acm.org/citation.cfm?id=1050933) by Michael Feathers.



One last piece of advice from a mentor of mine before we finish. If you find yourself creating a few example inputs for a function you developed in a notebook to check how the function is working, turn those examples into tests! This enables you to re-run that examples at any time to make sure they still work correctly. This is also a great place to start if you are struggling to get started writing tests!

Now, go out and start writing maintainable data science software with `pytest`!
