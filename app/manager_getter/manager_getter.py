# author: pubins.taylor
# modified date: 30 JAN 2024
# description: This module gets the manager data from ESPN Fantasy Baseball
# v0.1.0

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import os

espn_lg_member_base_url = "https://fantasy.espn.com/baseball/tools/leaguemembers?leagueId="


def get_managers(driver: webdriver.Chrome, lg_id: str) -> None:
    # fetch data
    driver.get(espn_lg_member_base_url + lg_id)
    # print("successfully navigated to " + league_member_base_url + lgID)
    driver.implicitly_wait(5)
    # get managers table
    try:
        managers_table = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Table"))).get_attribute("outerHTML")
    except Exception as e:
        exit(f"ERROR: could not find managers table. {e}")

    # print("successfully found managers table")
    driver.quit()
    # print("closed chrome driver")

    df = parse_managers(managers_table)

    export_managers_json(df)


def export_managers_json(df):
    # find the system path to /Shared/BaseballHQ/resources
    directory = '/Users/Shared/BaseballHQ/resources/extract'
    filename = 'lgmngrs.json'
    full_path = os.path.join(directory, filename)
    # write to json file
    # orienting on table adds schema information to the json file
    df.to_json(full_path, index=False, orient="table", indent=2)
    # print("JSON file created successfully...")


def parse_managers(managers_table):
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(managers_table, 'html.parser')
    # find the column index for the table header "MANAGER NAME"
    # Find the table header associated with the desired column
    desired_header = 'MANAGER NAME'
    header_cell = soup.find('th', string=desired_header)
    # Find the index of the header cell among its siblings
    column_index = header_cell.parent.index(header_cell)
    # print("found column index of " + desired_header + ": " + str(column_index))
    # Get the table rows
    table_rows = soup.find("tbody").find_all("tr")  # tbody is used to skip the header row
    # Create a new DataFrame
    df = pd.DataFrame(columns=["teamAbbreviation", "teamName", "teamOwner", "avatarURL"])
    # Print the found elements
    for team in table_rows:
        tmDetails = [team.find(class_="teamAbbrev").text, team.find(class_="teamName").text,
                     team.find_all('td')[column_index].text,
                     team.find(class_=["image-custom", "team-logo"]).find("img")["src"]]

        # Create a Series to append
        new_row = pd.Series(tmDetails, index=df.columns)
        # Use loc indexer to append the Series to the DataFrame
        df.loc[len(df)] = new_row
        # print("successfully added " + tmDetails[1] + " to dataframe")
    return df
