from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import lxml
import html5lib

myLgURL = "https://fantasy.espn.com/baseball/tools/leaguemembers?leagueId=10998"


def pullData():
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(myLgURL)
    driver.implicitly_wait(5)
    managersTable = driver.find_element(By.CLASS_NAME, "Table").get_attribute("outerHTML")
    driver.close()
    df = pd.read_html(managersTable)[0]
    managers = df[["ABBRV", "TEAM NAME", "MANAGER NAME"]]
    managers.to_json("managers.json", index=False, orient="table", indent=2)
    managers.to_csv("managers.csv", index=False)
    print(managers)



if __name__ == '__main__':
    pullData()
