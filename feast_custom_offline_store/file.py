from datetime import datetime
from typing import List, Optional, Union

import pandas as pd
from feast.data_source import DataSource
from feast.feature_view import FeatureView
from feast.infra.offline_stores.file import FileOfflineStore
from feast.infra.offline_stores.offline_store import RetrievalJob
from feast.registry import Registry
from feast.repo_config import RepoConfig, FeastConfigBaseModel
from pydantic.typing import Literal


class CustomFileOfflineStoreConfig(FeastConfigBaseModel):
    """ Custom offline store config for local (file-based) store """

    type: Literal["feast_custom_offline_store.file.CustomFileOfflineStore"] \
        = "feast_custom_offline_store.file.CustomFileOfflineStore"


class CustomFileOfflineStore(FileOfflineStore):
    def __init__(self):
        super().__init__()

    def get_historical_features(self,
                                config: RepoConfig,
                                feature_views: List[FeatureView],
                                feature_refs: List[str],
                                entity_df: Union[pd.DataFrame, str],
                                registry: Registry, project: str,
                                full_feature_names: bool = False) -> RetrievalJob:
        print("Getting historical features from my offline store")
        return super().get_historical_features(config,
                                               feature_views,
                                               feature_refs,
                                               entity_df,
                                               registry,
                                               project,
                                               full_feature_names)

    def pull_latest_from_table_or_query(self,
                                        config: RepoConfig,
                                        data_source: DataSource,
                                        join_key_columns: List[str],
                                        feature_name_columns: List[str],
                                        event_timestamp_column: str,
                                        created_timestamp_column: Optional[str],
                                        start_date: datetime,
                                        end_date: datetime) -> RetrievalJob:
        print("Pulling latest features from my offline store")
        return super().pull_latest_from_table_or_query(config,
                                                       data_source,
                                                       join_key_columns,
                                                       feature_name_columns,
                                                       event_timestamp_column,
                                                       created_timestamp_column,
                                                       start_date,
                                                       end_date)
