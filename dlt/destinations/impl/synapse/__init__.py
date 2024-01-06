from dlt.common.data_writers.escape import escape_postgres_identifier, escape_mssql_literal
from dlt.common.destination import DestinationCapabilitiesContext
from dlt.common.arithmetics import DEFAULT_NUMERIC_PRECISION, DEFAULT_NUMERIC_SCALE
from dlt.common.wei import EVM_DECIMAL_PRECISION


def capabilities() -> DestinationCapabilitiesContext:
    caps = DestinationCapabilitiesContext()

    caps.preferred_loader_file_format = "insert_values"
    caps.supported_loader_file_formats = ["insert_values"]
    caps.preferred_staging_file_format = "parquet"
    caps.supported_staging_file_formats = ["parquet"]

    caps.insert_values_writer_type = "select_union"

    caps.escape_identifier = escape_postgres_identifier
    caps.escape_literal = escape_mssql_literal

    # Synapse has a max precision of 38: https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-azure-sql-data-warehouse?view=aps-pdw-2016-au7#DataTypes
    caps.decimal_precision = (DEFAULT_NUMERIC_PRECISION, DEFAULT_NUMERIC_SCALE)
    caps.wei_precision = (DEFAULT_NUMERIC_PRECISION, 0)
    
    # https://learn.microsoft.com/en-us/sql/sql-server/maximum-capacity-specifications-for-sql-server?view=sql-server-ver16&redirectedfrom=MSDN
    caps.max_identifier_length = 128
    caps.max_column_identifier_length = 128
    caps.max_query_length = 4 * 1024 * 64 * 1024
    caps.is_max_query_length_in_bytes = True
    caps.max_text_data_type_length = 2**30 - 1
    caps.is_max_text_data_type_length_in_bytes = False
    caps.supports_ddl_transactions = False # https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-develop-transactions#limitations
    caps.max_rows_per_insert = 1000
    caps.timestamp_precision = 7

    return caps
