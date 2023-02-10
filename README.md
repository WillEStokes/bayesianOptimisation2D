# bayesianOptimisation2D

## BayesianOptimization Library Interaction Modules
This repository contains two modules for interacting with the BayesianOptimization library. The purpose of these modules is to provide an easy and efficient way for users to interact with the BayesianOptimization library and visualize the results of the optimisation process.

## Contents
- **`bayesianOptimisation.py`**: This module contains mostly wrapper functions that can be called from an external program. The functions provide a simple interface to perform Bayesian Optimization, which can be used to optimize any user-defined objective function.

- **`display.py`**: This module contains functions required to create a visually appealing 2D contour plot of the Gaussian process model and target values with matplotlib. The module provides an easy and intuitive way to visualize the optimization process and helps users to understand the behavior of the optimization algorithm.

## Requirements
- Python 3.x
- Json
- Shutil
- Numpy
- Matplotlib
- BayesianOptimization (https://github.com/fmfn/BayesianOptimization)
