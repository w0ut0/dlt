import dataclasses
from typing import ClassVar, Final, List, Optional

from dlt.common import logger
from dlt.common.configuration import configspec
from dlt.common.destination.reference import DestinationClientDwhWithStagingConfiguration
from dlt.common.configuration.specs import AwsCredentials


@configspec
class AthenaClientConfiguration(DestinationClientDwhWithStagingConfiguration):
    destination_type: Final[str] = dataclasses.field(default="athena", init=False, repr=False, compare=False)  # type: ignore[misc]
    query_result_bucket: str = None
    credentials: AwsCredentials = None
    athena_work_group: Optional[str] = None
    aws_data_catalog: Optional[str] = "awsdatacatalog"
    supports_truncate_command: bool = False
    force_iceberg: Optional[bool] = None

    __config_gen_annotations__: ClassVar[List[str]] = ["athena_work_group"]

    def on_resolved(self) -> None:
        if self.force_iceberg is not None:
            logger.warning(
                "force_iceberg flag is no longer supported. please set table format explicitly on"
                " the resources"
            )

    def __str__(self) -> str:
        """Return displayable destination location"""
        if self.staging_config:
            return str(self.staging_config.credentials)
        else:
            return "[no staging set]"
