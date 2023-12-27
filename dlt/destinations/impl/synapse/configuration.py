from typing import Final, Any, Optional, ClassVar

from dlt.common.configuration import configspec

from dlt.destinations.impl.mssql.configuration import (
    MsSqlCredentials,
    MsSqlClientConfiguration,
)
from dlt.destinations.impl.mssql.configuration import MsSqlCredentials


@configspec
class SynapseCredentials(MsSqlCredentials):
    # LongAsMax keyword got introduced in ODBC Driver 18 for SQL Server.
    SUPPORTED_DRIVERS: ClassVar[str] = ["ODBC Driver 18 for SQL Server"]

    def _get_odbc_dsn_dict(self) -> dict:
        params = super()._get_odbc_dsn_dict()
        # Long types (text, ntext, image) are not supported on Synapse.
        # Convert to max types using LongAsMax keyword.
        # https://stackoverflow.com/a/57926224 
        params["LONGASMAX"] = "yes"
        return params


@configspec
class SynapseClientConfiguration(MsSqlClientConfiguration):
    destination_type: Final[str] = "synapse"  # type: ignore
    credentials: SynapseCredentials
