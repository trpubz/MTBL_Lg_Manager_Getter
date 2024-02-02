import pytest
from app.driver_builder.driver_builder import build_driver


class TestDriverBuilder:
    def test_build_driver(self):
        driver = build_driver()
        assert driver is not None
        driver.get("https://www.google.com")
        assert "Google" in driver.title
        driver.quit()
