[![codecov](https://codecov.io/gh/trpubz/MTBL_Lg_Manager_Getter/graph/badge.svg?token=9QD3SE4NNQ)](https://codecov.io/gh/trpubz/MTBL_Lg_Manager_Getter)
# MTBL League Manager Getter


## Description
Applet needs to source an ESPN Fantasy Baseball League Managers page given a league ID.  
Base url is here https://fantasy.espn.com/baseball/tools/leaguemembers?leagueId={#lgid}.
This webscraping applet should get the team name, abbreviation, owner, and avatar URL.  
Output format is .json; see below for schema.

## Requirements
* MTBL ETL pipeline relies on a valid league ID and should be set in global environment vars
  * add to ~/.bash_profile or ~/.bashrc or ~/.zshrc: `MTBL_LGID={#your_lgid}`
  * verify it's existence with `echo $MTBL_LGID` from terminal
  * using python's `os.getenv("MTBL_LGID")` you will have access at the app execution
## Dependencies
* python >= 3.12
  * required in [setup.py]
  
## Output
```
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "teamName": {
      "type": "string"
    },
    "teamAbbreviation": {
      "type": "string"
    },
    "teamOwner": {
      "type": "string"
    },
    "avatarURL": {
      "type": "string",
      "format": "uri"
    }
  },
  "required": ["teamName", "teamAbbreviation", "teamOwner"]
}
```
