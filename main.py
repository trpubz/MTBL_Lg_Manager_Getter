# author: pubins.taylor
# modified date: 07 JUN 2023
# description: This script pulls data from ESPN Fantasy Baseball
# League and outputs a JSON file containing the team abbreviation, team name, team owner, and team avatar URL. The
# JSON file is used in the next step of my custom ETL pipeline as a keying device for league rosters pull. selenium 4
# v 1.1.0

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import pandas as pd
import os

# set league ID
lgID = "10998"
myLgURL = "https://fantasy.espn.com/baseball/tools/leaguemembers?leagueId=" + lgID


# Pulls data from ESPN Fantasy Baseball League
def pullData(sdrvr: webdriver.Chrome):
    # fetch data
    sdrvr.get(myLgURL)
    print("successfully navigated to " + myLgURL)
    sdrvr.implicitly_wait(5)
    # get managers table
    try:
        managersTable = WebDriverWait(sdrvr, 7).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "Table"))).get_attribute("outerHTML")
    except Exception as e:
        exit(f"ERROR: could not find managers table. {e}")

    print("successfully found managers table")
    sdrvr.quit()
    print("closed chrome driver")

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(managersTable, 'html.parser')
    # find the column index for the table header "MANAGER NAME"
    # Find the table header associated with the desired column
    desired_header = 'MANAGER NAME'
    header_cell = soup.find('th', string=desired_header)

    # Find the index of the header cell among its siblings
    column_index = header_cell.parent.index(header_cell)
    print("found column index of " + desired_header + ": " + str(column_index))

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
        print("successfully added " + tmDetails[1] + " to dataframe")

    print("successfully added all teams to dataframe")

    # find the system path to /Shared/BaseballHQ/resources
    directory = '/Users/Shared/BaseballHQ/resources/extract'
    filename = 'lgmngrs.json'
    full_path = os.path.join(directory, filename)

    # write to json file
    # orienting on table addes schema information to the json file
    df.to_json(full_path, index=False, orient="table", indent=2)
    print("JSON file created successfully...")


def buildDriver(headless=True) -> webdriver.Chrome:
    # set up headless chrome driver
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    # ChromeDriverManager().install() downloads latest version of chrome driver to avoid compatibility issues
    return webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))


def main():
    print("\n---starting Lg_Manager_Getter---\n")
    sdrvr = buildDriver(headless=True)
    pullData(sdrvr)
    print("\n---finished Lg_Manager_Getter---")


if __name__ == '__main__':
    main()
