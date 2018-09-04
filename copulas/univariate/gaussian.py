import logging

import numpy as np
import pandas as pd
from scipy.stats import norm

from copulas.univariate.base import Univariate

LOGGER = logging.getLogger(__name__)


class GaussianUnivariate(Univariate):
    """ Gaussian univariate model """

    def __init__(self):
        super().__init__()
        self.name = None
        self.mean = 0
        self.std = 1

    def __str__(self):
        details = [self.name, self.mean, self.std]
        return (
            'Distribution Type: Gaussian\n'
            'Variable name: {}\n'
            'Mean: {}\n'
            'Standard deviation: {}'.format(*details)
        )

    def fit(self, X):
        """Fits the model.

        Arguments:
            X: `np.ndarray` of shape (n, 1).

        Returns:
            None
        """

        if not len(X):
            raise ValueError("Can't fit with an empty dataset.")

        self.name = X.name if isinstance(X, pd.Series) else None
        self.mean = np.mean(X)
        self.std = np.std(X) or 0.001

    def probability_density(self, X):
        """Computes probability density.

        Arguments:
            X: `np.ndarray` of shape (n, 1).

        Returns:
            np.ndarray
        """
        return norm.pdf(X, loc=self.mean, scale=self.std)

    def cumulative_density(self, X):
        """Cumulative density function for gaussian distribution.

        Arguments:
            X: `np.ndarray` of shape (n, 1).

        Returns:
            np.ndarray: Cumulative density for X.
        """
        # check to make sure dtype is not object
        if X.dtype == 'object':
            X = X.astype('float64')

        return norm.cdf(X, loc=self.mean, scale=self.std)

    def percent_point(self, U):
        """Given a cumulated density, returns a value in original space.

        Arguments:
            U: `np.ndarray` of shape (n, 1) and values in [0,1]

        Returns:
            `np.ndarray`: Estimated values in original space.
        """
        return norm.ppf(U, loc=self.mean, scale=self.std)

    def sample(self, num_samples=1):
        """Returns new data point based on model.

        Arguments:
            n_samples: `int`

        Returns:
            np.ndarray: Generated samples
        """
        return np.random.normal(self.mean, self.std, num_samples)
