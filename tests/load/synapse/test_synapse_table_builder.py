import pytest
import sqlfluff

from dlt.common.utils import uniq_id
from dlt.common.schema import Schema

from dlt.destinations.impl.synapse.synapse import SynapseClient
from dlt.destinations.impl.synapse.configuration import (
    SynapseClientConfiguration,
    SynapseCredentials
)

from tests.load.utils import TABLE_UPDATE


@pytest.fixture
def schema() -> Schema:
    return Schema("event")


@pytest.fixture
def client(schema: Schema) -> SynapseClient:
    # return client without opening connection
    return SynapseClient(
        schema,
        SynapseClientConfiguration(
            dataset_name="test_" + uniq_id(), credentials=SynapseCredentials()
        ),
    )


def test_create_table(client: SynapseClient) -> None:
    # non existing table
    sql = client._get_table_update_sql("event_test_table", TABLE_UPDATE, False)[0]
    sqlfluff.parse(sql, dialect="tsql")
    assert "event_test_table" in sql
    assert '"col1" bigint  NOT NULL' in sql
    assert '"col2" float  NOT NULL' in sql
    assert '"col3" bit  NOT NULL' in sql
    assert '"col4" datetimeoffset  NOT NULL' in sql
    assert '"col5" nvarchar(max)  NOT NULL' in sql
    assert '"col6" decimal(38,9)  NOT NULL' in sql
    assert '"col7" varbinary(max)  NOT NULL' in sql
    assert '"col8" decimal(38,0)' in sql
    assert '"col9" nvarchar(max)  NOT NULL' in sql
    assert '"col10" date  NOT NULL' in sql
    assert '"col11" time  NOT NULL' in sql
    assert '"col1_precision" smallint  NOT NULL' in sql
    assert '"col4_precision" datetimeoffset(3)  NOT NULL' in sql
    assert '"col5_precision" nvarchar(25)' in sql
    assert '"col6_precision" decimal(6,2)  NOT NULL' in sql
    assert '"col7_precision" varbinary(19)' in sql
    assert '"col11_precision" time(3)  NOT NULL' in sql
    assert 'WITH ( HEAP )' in sql


def test_alter_table(client: SynapseClient) -> None:
    # existing table has no columns
    sql = client._get_table_update_sql("event_test_table", TABLE_UPDATE, True)[0]
    sqlfluff.parse(sql, dialect="tsql")
    canonical_name = client.sql_client.make_qualified_table_name("event_test_table")
    assert sql.count(f"ALTER TABLE {canonical_name}\nADD") == 1
    assert "event_test_table" in sql
    assert '"col1" bigint  NOT NULL' in sql
    assert '"col2" float  NOT NULL' in sql
    assert '"col3" bit  NOT NULL' in sql
    assert '"col4" datetimeoffset  NOT NULL' in sql
    assert '"col5" nvarchar(max)  NOT NULL' in sql
    assert '"col6" decimal(38,9)  NOT NULL' in sql
    assert '"col7" varbinary(max)  NOT NULL' in sql
    assert '"col8" decimal(38,0)' in sql
    assert '"col9" nvarchar(max)  NOT NULL' in sql
    assert '"col10" date  NOT NULL' in sql
    assert '"col11" time  NOT NULL' in sql
    assert '"col1_precision" smallint  NOT NULL' in sql
    assert '"col4_precision" datetimeoffset(3)  NOT NULL' in sql
    assert '"col5_precision" nvarchar(25)' in sql
    assert '"col6_precision" decimal(6,2)  NOT NULL' in sql
    assert '"col7_precision" varbinary(19)' in sql
    assert '"col11_precision" time(3)  NOT NULL' in sql
    assert 'WITH ( HEAP )' not in sql
