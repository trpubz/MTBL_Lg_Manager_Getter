# Lg_Manager_Getter


## Description
Applet needs to source an ESPN Fantasy Baseball League Managers page given a league ID.  Base url is here https://fantasy.espn.com/baseball/tools/leaguemembers?leagueId={#lgid}.
This webscraping applet should get the team name, abbreviation, owner, and avatar URL.  Output format is .json; see below for schema.

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
