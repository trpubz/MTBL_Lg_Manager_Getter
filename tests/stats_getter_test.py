import os

import pandas as pd
import pytest

from app.src.driver_builder import build_driver
from app.src.manager_getter import get_managers
from app.src.stats_getter import get_manager_stats


class TestStatsGetter:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = build_driver(headless=True)
        self.managers = get_managers(self.driver, os.getenv("MTBL_LGID"))
        yield
        self.driver.close()

    def test_get_stats(self):
        stats_df = get_manager_stats(self.driver, os.getenv("MTBL_LGID"), self.managers)

        assert stats_df.__class__ == pd.DataFrame
        assert stats_df.shape[0] == len(self.managers)
