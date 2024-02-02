import os

import pytest
from selenium.common import TimeoutException

from app.manager_getter.manager_getter import get_managers
from app.driver_builder.driver_builder import build_driver
import pandas as pd


class TestManagerGetter:
    driver = None

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.driver = build_driver()

    def test_get_managers(self):
        managers = get_managers(self.driver, os.getenv("MTBL_LGID"))
        assert managers.__class__ is pd.DataFrame
        assert len(managers) > 0

    def test_get_managers_no_table(self):
        with pytest.raises(TimeoutException) as te:
            _ = get_managers(self.driver, "invalid_league_id")

        assert te.type == TimeoutException

