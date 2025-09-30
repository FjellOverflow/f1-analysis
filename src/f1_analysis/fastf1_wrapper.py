from logging import getLogger
from pathlib import Path

import pandas as pd
from fastf1.core import Session
from pandas.core.frame import DataFrame

from f1_analysis.util import get_project_root

logger = getLogger(__name__)


class FastF1Wrapper:
    def __init__(self):
        self.__root_dir = Path(get_project_root()) / "data" / "fastf1"
        self.__root_dir.mkdir(parents=False, exist_ok=True)

    def __get_session_path(self, session: Session):
        season = session.event["EventDate"].year
        round = session.event["RoundNumber"]
        name = session.name.lower().replace(" ", ".")

        filename = f"{season}.{round}.{name}.laps.csv"

        return self.__root_dir / filename

    def load_session_laps(self, session: Session) -> DataFrame:
        local_path = self.__get_session_path(session)

        if local_path.is_file():
            return pd.read_csv(local_path)

        session.load(laps=True, telemetry=False, weather=False, messages=False)
        laps = session.laps

        laps.to_csv(local_path)

        logger.info(f"Cached session laps at {local_path}")

        return laps
