"""
author: pubins.taylor
modified date: 30 MAR 2024
description: This module gets the manager stats and append it to Dataframe from ESPN Fantasy
Baseball
v0.1.0
"""
import logging
from io import StringIO

import pandas as pd
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

ESPN_STATS_BASE_URL = "https://fantasy.espn.com/baseball/league/standings?leagueId="


def get_manager_stats(driver: webdriver, lg_id: str, df: pd.DataFrame) -> pd.DataFrame:
    # fetch data
    driver.get(ESPN_STATS_BASE_URL + lg_id)
    driver.implicitly_wait(5)
    try:
        managers_table = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.CLASS_NAME, "innerTable"))).get_attribute(
            "outerHTML")
        managers_table += driver.find_element(By.CLASS_NAME,
                                              "season--stats--table").get_attribute(
            "outerHTML")
    except TimeoutException as te:
        logging.error("ERROR: could not find managers table. %s", te)
        raise

    return parse_managers(df, managers_table)


def parse_managers(df: pd.DataFrame, managers_table: str) -> pd.DataFrame:
    """
    Parses managers from html string
    :param df: Dataframe containing the managers details from the League Managers page
    :param managers_table: html string
    :return: Dataframe
    """
    stats_dfs = pd.read_html(StringIO(managers_table))[:3]
    stats_dfs[2]['Team'] = stats_dfs[1]['Team']
    merged_df = df.copy()
    for i, stats_df in enumerate(stats_dfs):
        # Merge df with the current stat_df
        if i == 1 or i == 2:
            stats_df["Team"] = stats_df["Team"].apply(lambda x: x.split(" (")[0])
        if stats_df.columns.__class__ == pd.core.indexes.multi.MultiIndex:
            stats_df.columns = stats_df.columns.droplevel(0)
            stats_df.rename(columns={"": "Team"}, inplace=True)

        merged_df = merged_df.merge(stats_df,
                                    left_on="teamName",
                                    right_on="Team",
                                    suffixes=(None, "_x"))

        columns_to_drop = [col for col in merged_df.columns if col.endswith('_x')]
        merged_df.drop(columns=columns_to_drop, inplace=True)

    return merged_df.drop(columns=['Team'])

# def login(driver):
#     WebDriverWait(driver, 7).until(
#         EC.presence_of_element_located((By.XPATH, "//*[text()='Log In']")))
#     login_button = driver.find_element(By.XPATH, "//*[text()='Log In']")
#     sleep(2)
#     login_button.click()
#     driver.implicitly_wait(5)
#     email_input = driver.find_element(By.TAG_NAME, 'input')
#     driver.execute_script("arguments[0].value = arguments[1];", email_input, creds.email)
#
#     form = driver.find_element(By.XPATH, "//form")  # Adjust the locator to match the form element
#     driver.execute_script("arguments[0].submit();", form)
