"""
This module contains an example test.

Tests should be placed in ``tests``, in modules that mirror your
project's structure, and in files named test_*.py. They are simply functions
named ``test_*`` which test a unit of logic.

To run the tests, run ``pytest --cov -p no:warnings``.
"""
from pathlib import Path

import pytest

from src.train import train
from src import config, logger


@pytest.fixture
def project_config():
    return config


class TestTrainingPipeline:

    """Training Pipeline Integration Test"""

    def test_training_config_section(self, project_config):
        assert config.get("DATA") is not None
        assert config.get("MODEL") is not None
        assert config.get("TRAIN") is not None

    def test_credential_config_section(self, project_config):
        assert config.get("S3") is not None

    def test_training_pipeline(self):
        train()
