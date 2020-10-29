This directory contains code to support the "Hyperopt tips and tricks: Interactive visualization of hyperopt trials with plotly" blog post.

# Installation
Requires Python 3.6+. In a new virtual environment, run `pip install -r requirements.txt`.

# Download the notebook
The most recent version of the notebook is available to download at the following link:

[https://github.com/StatesTitle/ds-blog/blob/master/hyperopt_tips_and_tricks/interative_visualization_of_hyperopt_trials_with_plotly/interactive_visualization_of_hyperopt_trials_with_plotly.ipynb](https://github.com/StatesTitle/ds-blog/blob/master/hyperopt_tips_and_tricks/interative_visualization_of_hyperopt_trials_with_plotly/interactive_visualization_of_hyperopt_trials_with_plotly.ipynb)

In addition, you can view a static version of the notebook that includes the visualizations at the following link:

[https://statestitle.github.io/ds-blog/hyperopt_tips_and_tricks/interative_visualization_of_hyperopt_trials_with_plotly/interactive_visualization_of_hyperopt_trials_with_plotly.html](https://statestitle.github.io/ds-blog/hyperopt_tips_and_tricks/interative_visualization_of_hyperopt_trials_with_plotly/interactive_visualization_of_hyperopt_trials_with_plotly.html)

# Running the notebook
Run `ipython notebook` and select "interactive_visualization_of_hyperopt_trials_with_plotly.ipynb" to launch the notebook.

# Additional information
I recommend using `ipython notebook` to run the notebook since this avoids rendering issues with the plotly visualizations that you may encounter with `jupyter`. If you prefer to use `jupyter lab`, see these [instructions](https://plotly.com/python/getting-started/#jupyterlab-support-python-35) for installing a plugin to render plotly visualizations.

Note that the number of trials in the notebook is set to 1000 to replicate the results in the blog post. Running 1000 trials may take over an hour to run. As such, when you are first running through the notebook, you may want to set the number of trials to a smaller value to reduce the amount of time that it takes for the hyperparameter optimization to complete.
