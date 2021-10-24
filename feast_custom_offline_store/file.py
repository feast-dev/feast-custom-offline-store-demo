import json
from datetime import datetime
from typing import List, Optional, Union, Callable, Dict

import pandas as pd
import pyarrow
from feast import FileSource
from feast.data_source import DataSource
from feast.feature_view import FeatureView
from feast.infra.offline_stores.file import FileOfflineStore, FileRetrievalJob
from feast.infra.offline_stores.offline_store import RetrievalJob
from feast.registry import Registry
from feast.repo_config import RepoConfig, FeastConfigBaseModel
from pydantic.typing import Literal
from feast.protos.feast.core.DataSource_pb2 import DataSource as DataSourceProto


class CustomFileOfflineStoreConfig(FeastConfigBaseModel):
    """Custom offline store config for local (file-based) store"""

    type: Literal[
        "feast_custom_offline_store.file.CustomFileOfflineStore"
    ] = "feast_custom_offline_store.file.CustomFileOfflineStore"


class FileOfflineStoreConfig(FeastConfigBaseModel):
    """Offline store config for local (file-based) store"""

    type: Literal["file"] = "file"
    """ Offline store type selector"""


class CustomFileDataSource(FileSource):
    """Custom data source class for local files"""
    def __init__(
        self,
        event_timestamp_column: Optional[str] = "",
        path: Optional[str] = None,
        field_mapping: Optional[Dict[str, str]] = None,
        created_timestamp_column: Optional[str] = "",
        date_partition_column: Optional[str] = "",
    ):
        super(CustomFileDataSource, self).__init__(
            event_timestamp_column=event_timestamp_column,
            created_timestamp_column=created_timestamp_column,
            field_mapping=field_mapping,
            date_partition_column=date_partition_column,
            path=path,
        )
        self._path = path

    @property
    def path(self):
        """
        Returns the file path of this feature data source.
        """
        return self._path

    @staticmethod
    def from_proto(data_source: DataSourceProto):
        """
        Creates a `CustomFileDataSource` object from a DataSource proto, by
        parsing the CustomSourceOptions which is encoded as a binary json string.
        """
        custom_source_options = str(
            data_source.custom_options.configuration, encoding="utf8"
        )
        path = json.loads(custom_source_options)["path"]
        return CustomFileDataSource(
            field_mapping=dict(data_source.field_mapping),
            path=path,
            event_timestamp_column=data_source.event_timestamp_column,
            created_timestamp_column=data_source.created_timestamp_column,
            date_partition_column=data_source.date_partition_column,
        )

    def to_proto(self) -> DataSourceProto:
        """
        Creates a DataSource proto representation of this object, by serializing some
        custom options into the custom_options field as a binary encoded json string.
        """
        config_json = json.dumps({"path": self.path})
        data_source_proto = DataSourceProto(
            type=DataSourceProto.CUSTOM_SOURCE,
            field_mapping=self.field_mapping,
            custom_options=DataSourceProto.CustomSourceOptions(
                configuration=bytes(config_json, encoding="utf8")
            ),
        )

        data_source_proto.event_timestamp_column = self.event_timestamp_column
        data_source_proto.created_timestamp_column = self.created_timestamp_column
        data_source_proto.date_partition_column = self.date_partition_column

        return data_source_proto

    def get_table_query_string(self) -> str:
        pass


class CustomFileRetrievalJob(RetrievalJob):
    def __init__(self, evaluation_function: Callable):
        """Initialize a lazy historical retrieval job"""

        # The evaluation function executes a stored procedure to compute a historical retrieval.
        self.evaluation_function = evaluation_function

    @property
    def full_feature_names(self):
        return False

    @property
    def on_demand_feature_views(self):
        return None

    def _to_df_internal(self):
        # Only execute the evaluation function to build the final historical retrieval dataframe at the last moment.
        print("Getting a pandas DataFrame from a File is easy!")
        df = self.evaluation_function()
        return df

    def _to_arrow_internal(self):
        # Only execute the evaluation function to build the final historical retrieval dataframe at the last moment.
        print("Getting an arrow Table from a File is easy!")
        df = self.evaluation_function()
        return pyarrow.Table.from_pandas(df)


class CustomFileOfflineStore(FileOfflineStore):
    def __init__(self):
        super().__init__()

    def get_historical_features(
        self,
        config: RepoConfig,
        feature_views: List[FeatureView],
        feature_refs: List[str],
        entity_df: Union[pd.DataFrame, str],
        registry: Registry,
        project: str,
        full_feature_names: bool = False,
    ) -> RetrievalJob:
        print("Getting historical features from my offline store")
        job = super().get_historical_features(
            config,
            feature_views,
            feature_refs,
            entity_df,
            registry,
            project,
            full_feature_names,
        )
        assert isinstance(job, FileRetrievalJob)
        return CustomFileRetrievalJob(job.evaluation_function)

    def pull_latest_from_table_or_query(
        self,
        config: RepoConfig,
        data_source: DataSource,
        join_key_columns: List[str],
        feature_name_columns: List[str],
        event_timestamp_column: str,
        created_timestamp_column: Optional[str],
        start_date: datetime,
        end_date: datetime,
    ) -> RetrievalJob:
        print("Pulling latest features from my offline store")
        job = super().pull_latest_from_table_or_query(
            config,
            data_source,
            join_key_columns,
            feature_name_columns,
            event_timestamp_column,
            created_timestamp_column,
            start_date,
            end_date,
        )
        assert isinstance(job, FileRetrievalJob)
        return CustomFileRetrievalJob(job.evaluation_function)
