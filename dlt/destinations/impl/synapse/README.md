Execute the following SQL statements to set up the `loader` user:
```sql
-- on master database

CREATE LOGIN loader WITH PASSWORD = 'YOUR_PASSWORD_HERE';
```

```sql
-- on minipool database

CREATE USER loader FOR LOGIN loader;

-- DDL permissions
GRANT CREATE TABLE ON DATABASE :: minipool TO loader;
GRANT CREATE VIEW ON DATABASE :: minipool TO loader;

-- DML permissions
GRANT SELECT ON DATABASE :: minipool TO loader;
GRANT INSERT ON DATABASE :: minipool TO loader;
GRANT ADMINISTER DATABASE BULK OPERATIONS TO loader;
```
