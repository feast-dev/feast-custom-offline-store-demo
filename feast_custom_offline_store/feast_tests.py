import tempfile
from typing import Any, Dict, List, Optional

import pandas as pd

from feast.data_source import DataSource
from feast.repo_config import FeastConfigBaseModel

from feast_custom_offline_store.file import CustomFileDataSource, CustomFileOfflineStoreConfig
from tests.integration.feature_repos.integration_test_repo_config import (
    IntegrationTestRepoConfig,
)
from tests.integration.feature_repos.universal.data_source_creator import (
    DataSourceCreator,
)
from tests.integration.feature_repos.universal.data_sources.file import (
    FileDataSourceCreator,
)

class CustomFileDataSourceCreator(DataSourceCreator):
    files: List[Any]

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.files = []

    def create_data_source(
        self,
        df: pd.DataFrame,
        destination_name: str,
        event_timestamp_column="ts",
        created_timestamp_column="created_ts",
        field_mapping: Dict[str, str] = None,
    ) -> DataSource:

        destination_name = self.get_prefixed_table_name(destination_name)

        f = tempfile.NamedTemporaryFile(
            prefix=f"{self.project_name}_{destination_name}",
            suffix=".parquet",
            delete=False,
        )
        df.to_parquet(f.name)
        self.files.append(f)
        return CustomFileDataSource(
            path=f"{f.name}",
            event_timestamp_column=event_timestamp_column,
            created_timestamp_column=created_timestamp_column,
            date_partition_column="",
            field_mapping=field_mapping or {"ts_1": "ts"},
        )

    def get_prefixed_table_name(self, suffix: str) -> str:
        return f"{self.project_name}.{suffix}"

    def create_offline_store_config(self) -> FeastConfigBaseModel:
        return CustomFileOfflineStoreConfig()

    def teardown(self):
        for f in self.files:
            f.close()


FULL_REPO_CONFIGS = [
    IntegrationTestRepoConfig(),
    IntegrationTestRepoConfig(
        provider="local",
        offline_store_creator=CustomFileDataSourceCreator,
    )
]