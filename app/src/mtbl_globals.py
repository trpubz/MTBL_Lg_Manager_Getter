# File with global variables
# by pubins.taylor
# v0.6.3
# lastUpdate 27 MAR 2024
from enum import Enum

DIR_EXTRACT = "/Users/Shared/BaseballHQ/resources/extract"
DIR_TRANSFORM = "/Users/Shared/BaseballHQ/resources/transform"
MTBL_KEYMAP_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSEw6LWoxJrrBSFY39wA_PxSW5SG_t3J7dJT3JsP2DpMF5vWY6HJY071d8iNIttYDnArfQXg-oY_Q6I/pubhtml?gid=0&single=true"
# the names of the stat columns from Fangraphs downloaded csvs
HITTER_STATS = ["Name", "Team", "G", "PA", "HR", "R", "RBI", "SB", "CS", "BB%", "K%", "ISO",
                "BABIP", "AVG", "OBP", "SLG", "xSLG", "wOBA", "xwOBA", "wRC+", "wRAA", "EV",
                "Barrel%", "HardHit%", "PlayerId", "MLBAMID"]
PITCHER_STATS = ["Name", "Team", "G", "GS", "IP", "SV", "HLD", "ERA", "xERA", "WHIP", "FIP",
                 "xFIP", "SIERA", "K/9", "BB/9", "K/BB", "EV", "Barrel%", "HardHit%", "PlayerId",
                 "MLBAMID"]  # add QS during merge
# ESPN CONFIG
NO_MANAGERS = 11
LG_RULESET = {
    "ROSTER_SIZE": 21,
    "BENCH_SLOTS": 5,
    "DRAFT_BUDGET": 260,
    "SCORING": {
        "BATTING": [
            "R", "HR", "RBI", "SBN", "OBP", "SLG"
        ],
        "PITCHING": [
            "IP", "QS", "ERA", "WHIP", "K/9", "SVHD"
        ]
    },
    "ROSTER_REQS": {
        "BATTERS": {
            "C": 1,
            "1B": 1,
            "2B": 1,
            "3B": 1,
            "SS": 1,
            "OF": 3,
            "DH": 1,
        },
        "BENCH": 5,
        "PITCHERS": {
            "SP": 3,
            "RP": 2,
            "P": 2
        }
    }
}


class ETLType(Enum):
    PRE_SZN = "preseason"
    REG_SZN = "regular_season"

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return self.name

    @staticmethod
    def from_string(s):
        try:
            return ETLType[s]
        except KeyError:
            raise ValueError()


class FGProjSys(Enum):
    DC_ROS = "rfangraphsdc"
    ZIPS_ROS = "rzips"
    STEAMER_ROS = "steamerr"
    ATC_DC_ROS = "ratcdc"
    BATX_ROS = "rthebatx"

    ATC = "atc"
    DC = "fangraphsdc"
    BATX = "thebatx"
    BAT = "thebat"


class FGStatGroup(Enum):
    # For Fantasy Stat Type
    FANTASY = "fantasy"
    ADVANCED = "advanced"
    STANDARD = "standard"
    DASHBOARD = "dashboard"


class FGFantasyPreset(Enum):
    # the default is dashboard if anything other than FGStatGroup.FANTASY is chosen
    DASHBOARD = "dashboard"
    CLASSIC = "classic"


class FGStats(Enum):
    # For in-season stats
    STD = "0"
    ADV = "1"
    STCST = "24"


class FGPosGrp(Enum):
    HIT = 'bat'
    PIT = 'pit'


class BRefStats(Enum):
    PIT = "starter-pitching"


class Savant(Enum):
    XSTATS = "expected_statistics"
    BARRELS = "statcast"
    ROLLING = "rolling"
    RANKINGS = "percentile-rankings"
    ARSENAL_STATS = "pitch-arsenal-stats"
    CUSTOM = "custom"


class SavantDownload(Enum):
    XSTATS = "expected_stats"
    BARRELS = "exit_velocity"
    # rolling does not download .csv; need to webscrape
    RANKINGS = "percentile-rankings"
    ARSENAL_STATS = "pitch-arsenal-stats"
    CUSTOM = "stats"


class SavantPosGrp(Enum):
    HIT = "batter"
    PIT = "pitcher"


class SavantStatCategories(Enum):
    # https://baseballsavant.mlb.com/leaderboard/custom?year=2023&type=batter&filter=&sort=1&sortDir=desc&min=10&selections=ab,pa,hit,home_run,k_percent,bb_percent,batting_avg,slg_percent,on_base_percent,on_base_plus_slg,b_rbi,r_total_caught_stealing,r_total_stolen_base,r_run,woba,xwoba,exit_velocity_avg,sweet_spot_percent,barrel_batted_rate,hard_hit_percent,oz_swing_percent,n_bolts,&chart=false&x=ab&y=ab&r=no&chartType=beeswarm
    AB = "ab"
    PA = "pa"
    H = "hit"
    HR = "home_run"
    k_pct = "k_percent"
    bb_pct = "bb_percent"
    AVG = "batting_avg"
    SLG = "slg_percent"
    xSLG = "xslg"
    OBP = "on_base_percent"
    xOBP = "xobp"
    OPS = "on_base_plus_slg"
    xISO = "xiso"
    RBI = "b_rbi"
    CS = "r_total_caught_stealing"
    SB = "r_total_stolen_base"
    R = "r_run"
    wOBA = "woba"
    xwOBA = "xwoba"
    ev = "exit_velocity_avg"
    ev50 = "avg_best_speed"  # For a batter, EV50 is an average of the hardest 50% of his batted
    # balls. For a pitcher it is the average of his softest 50% of batted balls allowed.
    adj_ev = "avg_hyper_speed"  # Adjusted EV averages the maximum of 88 and the actual exit
    # velocity of each batted ball event.
    swt_spt_pct = "sweet_spot_percent"
    barrel_pct = "barrel_batted_rate"
    hard_hit_pct = "hard_hit_percent"
    oz_swing_pct = "oz_swing_percent"
    bolts = "n_bolts"
    # https://baseballsavant.mlb.com/leaderboard/custom?year=2023&type=pitcher&filter=&sort=4&sortDir=asc&min=q&selections=p_game,p_formatted_ip,pa,hit,home_run,strikeout,walk,k_percent,bb_percent,p_save,p_era,p_quality_start,p_hold,p_starting_p,woba,xwoba,exit_velocity_avg,sweet_spot_percent,barrel_batted_rate,hard_hit_percent,oz_swing_percent,whiff_percent,&chart=false&x=p_game&y=p_game&r=no&chartType=beeswarm
    G = "p_game"
    IP = "p_formatted_ip"
    K = "strikeout"
    BB = "walk"
    ERA = "p_era"
    QS = "p_quality_start"
    SV = "p_save"
    HLD = "p_hold"
    GS = "p_starting_p"
    wiff_pct = "whiff_percent"
    swing_pct = "swing_percent"
