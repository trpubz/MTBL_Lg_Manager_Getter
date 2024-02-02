"""
author: pubins.taylor
modified date: 30 JAN 2024
description: This script pulls data from ESPN
Fantasy Baseball League and outputs a JSON file containing the team abbreviation, team name,
team owner, and team avatar URL. The JSON file is used in the next step of my custom ETL
pipeline as a keying device for league rosters pull.
v3.0.0
"""
import os
import argparse

from mtbl_savekit.exporter import export_dataframe
from app.driver_builder.driver_builder import build_driver
from app.manager_getter.manager_getter import get_managers


def main(lg_id):
    """
    Build the driver and get the managers for a given league and export
    :param lg_id: ESPN league ID
    :return: None
    """
    print("\n---starting Lg_Manager_Getter---\n")
    driver = build_driver()
    managers_df = get_managers(driver, lg_id)
    export_dataframe(managers_df, "lgmngrs", ".json")
    print("\n---finished Lg_Manager_Getter---")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process league ID.")
    parser.add_argument(
        "--lgID",
        type=str, help="League ID",
        default=os.getenv("MTBL_LGID", 'default value'))

    args = parser.parse_args()
    main(args.lgID)
