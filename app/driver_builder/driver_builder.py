"""
author: pubins.taylor
modified date: 30 JAN 2024
description: module that builds the driver
v0.1.0
"""
import os
from mtbl_driverkit import mtbl_driverkit as DK
from selenium import webdriver


def build_driver(headless=True) -> webdriver.Chrome:
    """
    Wrapper function for driverkit.dk_driver_config()
    :param headless: True or False
    :return: selenium webdriver
    """
    driver, _ = DK.dk_driver_config(os.getcwd(), headless=headless)
    return driver
