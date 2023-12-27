from typing import ClassVar, Sequence, List

from dlt.common.destination import DestinationCapabilitiesContext
from dlt.common.destination.reference import SupportsStagingDestination

from dlt.common.schema import TColumnSchema, Schema
from dlt.common.schema.typing import TTableSchemaColumns

from dlt.destinations.insert_job_client import InsertValuesJobClient
from dlt.destinations.job_client_impl import SqlJobClientBase

from dlt.destinations.impl.mssql.mssql import MsSqlTypeMapper, MsSqlClient, HINT_TO_MSSQL_ATTR

from dlt.destinations.impl.synapse import capabilities
from dlt.destinations.impl.synapse.sql_client import SynapseSqlClient
from dlt.destinations.impl.synapse.configuration import SynapseClientConfiguration


class SynapseClient(MsSqlClient, SupportsStagingDestination):
    capabilities: ClassVar[DestinationCapabilitiesContext] = capabilities()

    def __init__(self, schema: Schema, config: SynapseClientConfiguration) -> None:   
        sql_client = SynapseSqlClient(config.normalize_dataset_name(schema), config.credentials)
        InsertValuesJobClient.__init__(self, schema, config, sql_client)
        self.config: SynapseClientConfiguration = config
        self.sql_client = sql_client
        self.active_hints = HINT_TO_MSSQL_ATTR if self.config.create_indexes else {}
        self.type_mapper = MsSqlTypeMapper(self.capabilities)

    def _get_table_update_sql(
        self, table_name: str, new_columns: Sequence[TColumnSchema], generate_alter: bool
    ) -> List[str]:
        _sql_result = SqlJobClientBase._get_table_update_sql(
            self, table_name, new_columns, generate_alter
        )
        if not generate_alter:
            # Append WITH clause to create heap table instead of default
            # columnstore table. Heap tables are a more robust choice, because
            # columnstore tables do not support varchar(max), nvarchar(max),
            # and varbinary(max).
            # https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-tables-index
            sql_result = [_sql_result[0] + "\n WITH ( HEAP );"]
        else:
            sql_result = _sql_result
        return sql_result


