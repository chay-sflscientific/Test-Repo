# -*- coding: utf-8 -*-

"""Example code for the Model Module. This code is meant
just for illustrating basic SFL Template features.

Delete this when you start working on your own SFL project.
"""

from src import logger
import dill
import xgboost as xgb
import re
import os
import ast
import sys
import glob
import logging

import warnings

warnings.filterwarnings("ignore")


# ------------------------------------------------------------------------------#
#                                 LOGGER                                   #
# ------------------------------------------------------------------------------#


# ------------------------------------------------------------------------------#
#                                MODEL                                         #
# ------------------------------------------------------------------------------#


class ExampleModel(xgb.XGBClassifier):
    """
    Dummy XGBoost model

    Methods:
    --------

    save:
        Save XGBmodel into save_dir
    load:
        Load XGBmodel from save_dir

    """

    def save(self, save_dir=""):
        """Save XGBModel to input path"""
        with open(save_dir, "wb") as f:
            dill.dump(self, f)

    @staticmethod
    def load(save_dir=""):
        """Load XGBModel from input path"""
        with open(save_dir, "rb") as f:
            return dill.load(f)
