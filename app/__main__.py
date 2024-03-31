"""
author: pubins.taylor
modified date: 30 MAR 2024
description: This script pulls data from ESPN
Fantasy Baseball League and outputs a JSON file containing the team abbreviation, team name,
team owner, and team avatar URL. The JSON file is used in the next step of my custom ETL
pipeline as a keying device for league rosters pull.
v4.0.0
"""
import os
import argparse

from mtbl_savekit.exporter import export_dataframe
from app.src.driver_builder import build_driver
from app.src.manager_getter import get_managers
from app.src.mtbl_globals import ETLType
from app.src.stats_getter import get_manager_stats


def main(lg_id: str, etl_type: ETLType):
    """
    Build the driver and get the managers for a given league and export
    :param etl_type: PRE_SZN or REG_SZN
    :param lg_id: ESPN league ID
    :return: None
    """
    print("\n---starting Lg_Manager_Getter---\n")
    driver = build_driver()
    managers_df = get_managers(driver, lg_id)
    if etl_type == ETLType.REG_SZN:
        managers_df = get_manager_stats(driver, lg_id, managers_df)

    driver.close()

    export_dataframe(managers_df, "lg_managers", ".json")

    print("\n---finished Lg_Manager_Getter---")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process league ID.")
    parser.add_argument(
        "--lgID",
        type=str, help="League ID",
        default=os.getenv("MTBL_LGID", 'default value'))

    parser.add_argument(
        "--etl-type",
        type=ETLType.from_string,
        choices=list(ETLType),
        help="ETL Type; PRE_SZN or REG_SZN",
        default=ETLType.REG_SZN)

    args = parser.parse_args()
    main(args.lgID, args.etl_type)
