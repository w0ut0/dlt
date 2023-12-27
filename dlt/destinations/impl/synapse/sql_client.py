from contextlib import suppress

from dlt.destinations.impl.mssql.sql_client import PyOdbcMsSqlClient
from dlt.destinations.impl.mssql.configuration import MsSqlCredentials
from dlt.destinations.impl.synapse.configuration import SynapseCredentials

from dlt.destinations.exceptions import DatabaseUndefinedRelation


class SynapseSqlClient(PyOdbcMsSqlClient):
    def drop_tables(self, *tables: str) -> None:
        if not tables:
            return
        # Synapse does not support DROP TABLE IF EXISTS.
        # Workaround: use DROP TABLE and suppress non-existence errors.
        statements = [
            f"DROP TABLE {self.make_qualified_table_name(table)};" for table in tables
        ]
        with suppress(DatabaseUndefinedRelation):
            self.execute_fragments(statements)        
        

    def drop_dataset(self) -> None:
        # MS Sql doesn't support DROP ... CASCADE, drop tables in the schema first
        # Drop all views
        rows = self.execute_sql(
            "SELECT table_name FROM information_schema.views WHERE table_schema = %s;",
            self.dataset_name,
        )
        view_names = [row[0] for row in rows]
        self._drop_views(*view_names)
        # Drop all tables
        rows = self.execute_sql(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = %s;",
            self.dataset_name,
        )
        table_names = [row[0] for row in rows]
        self.drop_tables(*table_names)

        self.execute_sql("DROP SCHEMA %s;" % self.fully_qualified_dataset_name())