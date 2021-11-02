# -*- coding: utf-8 -*-
"""Example code for the Transform functions. This code is meant
just for illustrating basic SFL Template features.

Update this when you start working on your own SFL project.
"""

from src import config
from src import logger
from src.classes.transform import Transform, TfmType
from sys import path as sys_path
from os import path as os_path
from pathlib import Path
import re
import os
import ast
import csv
import glob
import copy

import logging
import subprocess
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


# ------------------------------------------------------------------------------#
#                                 LOGGER                                   #
# ------------------------------------------------------------------------------#


# ------------------------------------------------------------------------------#
#                                 CONFIG                                   #
# ------------------------------------------------------------------------------#


# ------------------------------------------------------------------------------#
#                                 PARAMETERS                                   #
# ------------------------------------------------------------------------------#

EXAMPLE_TEST_DATA_RATIO = config.get("TRAIN").get("EXAMPLE_TEST_DATA_RATIO")


class ExampleTransform(Transform):

    """
    Tansform function placeholder

    Arguments:
    ---------
        df(pd.DataFrame):
            Input dataframe

                        |target|
            ------------------------------------
            Index 1|  <YOUR-GT>|
            ------------------------------------
            Index 2|  <YOUR-GT>|
            ------------------------------------
            Index 3|  <YOUR-GT>|
            ------------------------------------
            Index 4|  <YOUR-GT>|

    Returns
    -------
        df(pd.DataFrame):
            Same as input df.

    """

    def __init__(self, tfm_y=TfmType.NO):
        super(ExampleTransform, self).__init__(tfm_y)

    def transform(self, df):

        from sklearn.preprocessing import LabelEncoder

        label_encoder = LabelEncoder()
        label_encoder.fit(df["target"])
        df["target"] = label_encoder.transform(df["target"])

        return df
