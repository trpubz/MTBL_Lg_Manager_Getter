"""
author: pubins.taylor
modified date: 30 MAR 2024
description: This module gets the manager data from ESPN Fantasy Baseball
v0.2.1
"""
import logging

from pandas import DataFrame
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

ESPN_LG_BASE_URL = "https://fantasy.espn.com/baseball/tools/leaguemembers?leagueId="


def get_managers(driver: webdriver.Chrome, lg_id: str) -> DataFrame:
    """
    Get the managers for a given league
    :param driver: pre-built selenium webdriver
    :param lg_id: ESPN league ID
    :return: full parsed dataframe of managers
    """
    # fetch data
    driver.get(ESPN_LG_BASE_URL + lg_id)
    driver.implicitly_wait(5)
    # find managers table
    try:
        managers_table = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Table"))).get_attribute("outerHTML")
    except TimeoutException as te:
        logging.error("ERROR: could not find managers table. %s", te)
        raise

    return parse_managers(managers_table)


def parse_managers(managers_table) -> pd.DataFrame:
    """
    Parse the managers table
    :param managers_table: HTML div table containing managers
    :return: pandas dataframe of managers
    """
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
