"""Script with coordinates utils."""

from enum import Enum

import numpy as np
import pandas as pd


class GoalCoordinates(Enum):
    X = 89
    Y = 0


def get_normalized_coordinate(df: pd.DataFrame, coord_type: str) -> pd.Series:
    def normalize_coordinate(row: dict, coord_type: str) -> int:
        home_team_defending_side = row["home_team_defending_side"]
        home_team_id = row["home_team_id"]
        event_owner_team_id = row["event_owner_team_id"]
        coord = row[f"{coord_type}_coord"]

        if (home_team_defending_side == "left" and home_team_id != event_owner_team_id) or (
            home_team_defending_side == "right" and home_team_id == event_owner_team_id
        ):
            return coord * (-1)

        return coord

    return df.apply(lambda row: normalize_coordinate(row=row, coord_type=coord_type), axis=1)


def get_distance_from_goal(df: pd.DataFrame) -> pd.Series:
    """Compute distance from goal in feet."""
    return np.sqrt(
        (df["x_coord_norm"] - GoalCoordinates.X.value) ** 2 + (df["y_coord_norm"] - GoalCoordinates.Y.value) ** 2
    )


def get_angle(df: pd.DataFrame) -> pd.Series:
    return np.degrees(np.arctan2(df["y_coord_norm"].abs(), GoalCoordinates.X.value - df["x_coord_norm"].abs()))


def get_combination(df: pd.DataFrame, cols: list, sep: str = ",") -> pd.Series:
    """Create a text combination of `cols`, separetad by `sep`."""
    return df.loc[:, cols].astype(str).apply(sep.join, axis=1)


def get_zone(df: pd.DataFrame) -> pd.Series:
    def determine_zone(row: dict):
        x = row["x_coord_norm"]
        y = row["y_coord_norm"]

        if x < 20:
            return "neutral"
        elif 20 <= x <= 50:
            return "blue line"
        elif 50 <= x <= 80 and 15 < y <= 40:
            return "circle"  # left
        elif 50 <= x <= 80 and -40 <= y < -15:
            return "circle"  # right
        elif 50 <= x <= 75 and -15 <= y <= 15:
            return "high slot"
        elif 75 <= x <= 90 and -15 <= y <= 15:
            return "low slot"
        elif 80 <= x <= 100 and 15 < y <= 43:
            return "point"  # left
        elif 80 <= x <= 100 and -43 <= y < -15:
            return "point"  # right
        elif 90 < x <= 100 and -10 <= y <= 10:
            return "behind the net"
        else:
            return "other"

    return df.apply(lambda row: determine_zone(row=row), axis=1)
