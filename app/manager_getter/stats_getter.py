"""
author: pubins.taylor
modified date: 30 MAR 2024
description: This module gets the manager stats and append it to Dataframe from ESPN Fantasy
Baseball
v0.1.
"""
import logging

import pandas as pd
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

ESPN_STATS_BASE_URL = "https://fantasy.espn.com/baseball/league/standings?leagueid="


def get_manager_stats(driver: webdriver, lg_id: str, df: pd.DataFrame) -> pd.DataFrame:
    # fetch data
    driver.get(ESPN_STATS_BASE_URL + lg_id)
    driver.implicitly_wait(5)
    try:
        if len(driver.find_elements(By.XPATH, "//*[contains(text(), 'Log in Required')]")) > 0:
            login(driver)
        managers_table = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.CLASS_NAME, "innerTable"))).get_attribute(
            "outerHTML")
    except TimeoutException as te:
        logging.error("ERROR: could not find managers table. %s", te)
        raise

    stats_df = pd.read_html(managers_table)
    return df.merge(stats_df, inner_on="teamName")


def login(driver):
    login_button = driver.find_element(By.XPATH, "//*[text()='Log In']")
    login_button.click()
    driver.find_element(By.TAG_NAME, "input").send_keys(Keys)


def parse_stats(managers_table: str) -> pd.DataFrame:
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(managers_table, 'html.parser')
    desired_header = 'MANAGER NAME'
    header_cell = soup.find('th', string=desired_header)
    # Find the index of the header cell among its siblings
    column_index = header_cell.parent.index(header_cell)
    table_rows = soup.find("tbody").find_all("tr")  # tbody is used to skip the header row

    df = pd.DataFrame(columns=["teamAbbreviation", "teamName", "teamOwner", "avatarURL"])

    for team in table_rows:
        team_details = [team.find(class_="teamAbbrev").text, team.find(class_="teamName").text,
                        team.find_all('td')[column_index].text,
                        team.find(class_=["image-custom", "team-logo"]).find("img")["src"]]

        # Create a Series to append
        new_row = pd.Series(team_details, index=df.columns)
        # Use loc indexer to append the Series to the DataFrame
        df.loc[len(df)] = new_row

    return df
