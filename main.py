# author: pubins.taylor
# modified date: 18MAY2023
# description: This script pulls data from ESPN Fantasy Baseball League and outputs a JSON file
#              containing the team abbreviation, team name, team owner, and team avatar URL.
#              The JSON file is used in the next step of my custom ETL pipeline as a keying device for league rosters pull.
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import pandas as pd
import lxml # required for pd.read_html

# set league ID
lgID = "10998"
myLgURL = "https://fantasy.espn.com/baseball/tools/leaguemembers?leagueId=" + lgID

# Pulls data from ESPN Fantasy Baseball League
def pullData():
    # set up headless chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    # ChromeDriverManager().install() downloads latest version of chrome driver to avoid compatibility issues
    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    # fetch data
    driver.get(myLgURL)
    driver.implicitly_wait(5)
    # get managers table
    managersTable = driver.find_element(By.CLASS_NAME, "Table").get_attribute("outerHTML")
    driver.close()
    
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(managersTable, 'html.parser')
    # find the column index for the table header "MANAGER NAME"
    # Find the table header associated with the desired column
    desired_header = 'MANAGER NAME'
    header_cell = soup.find('th', text=desired_header)

    # Find the index of the header cell among its siblings
    column_index = header_cell.parent.index(header_cell)
    
    # Get the table rows
    table_rows = soup.find("tbody").find_all("tr") # tbody is used to skip the header row
    # Create a new DataFrame
    df = pd.DataFrame(columns=["teamAbbreviation", "teamName", "teamOwner", "avatarURL"])
    # Print the found elements
    for team in table_rows:
        tmDetails = []
        tmDetails.append(team.find(class_="teamAbbrev").text) #  team abbreviation
        tmDetails.append(team.find(class_="teamName").text) # team name
        tmDetails.append(team.find_all('td')[column_index].text) # team owner
        tmDetails.append(team.find(class_=["image-custom","team-logo"]).find("img")["src"]) # team avatar
        
        # Create a Series to append
        new_row = pd.Series(tmDetails, index=df.columns)
        # Use loc indexer to append the Series to the DataFrame
        df.loc[len(df)] = new_row
        
    print(df)
    # write to json file
    df.to_json("lgmngrs.json", index=False, orient="table", indent=2)

if __name__ == '__main__':
    pullData()
