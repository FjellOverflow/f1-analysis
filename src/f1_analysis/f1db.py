import sqlite3
import zipfile
from logging import getLogger
from pathlib import Path

import requests

from f1_analysis.util import get_github_latest_release_tag, get_project_root

logger = getLogger(__name__)


class F1DB:
    def __init__(self):
        self.__root_dir = Path(get_project_root()) / "data" / "f1db"
        self.__root_dir.mkdir(parents=False, exist_ok=True)

        self.__db_path = self.__root_dir / "f1db.db"
        self.__zip_path = self.__root_dir / "f1db.zip"
        self.__tag_path = self.__root_dir / "f1db.tag"

        self.__update()

    def __get_local_tag(self):
        if self.__tag_path.is_file():
            return self.__tag_path.read_text(encoding="utf-8")

    def __download_and_extract(self):
        response = requests.get(
            "https://github.com/f1db/f1db/releases/latest/download/f1db-sqlite.zip"
        )
        response.raise_for_status()

        self.__zip_path.write_bytes(response.content)

        with zipfile.ZipFile(self.__zip_path, "r") as archive:
            archive.extract("f1db.db", path=self.__root_dir)

    def __update(self):
        latest_tag = get_github_latest_release_tag("f1db", "f1db")

        if self.__get_local_tag() == latest_tag:
            return

        self.__download_and_extract()
        self.__tag_path.write_text(latest_tag, encoding="utf-8")

        logger.info(f"Updated local f1db to tag {latest_tag}")

    def __connect(self):
        file_uri = f"file:{self.__db_path}?mode=ro"
        return sqlite3.connect(file_uri, uri=True)

    def execute_raw_sql_query(self, sql_query: str):
        connection = self.__connect()
        cursor = connection.cursor()

        cursor.execute(sql_query)
        result = cursor.fetchall()

        connection.close()
        return result

    def execute_sql_query(self, sql_query_name: str):
        sql_query_path = get_project_root() / "sql" / sql_query_name

        if not sql_query_path.is_file():
            raise FileNotFoundError(f"File {sql_query_path} does not exist.")

        sql_query = sql_query_path.read_text(encoding="utf-8")

        return self.execute_raw_sql_query(sql_query)
