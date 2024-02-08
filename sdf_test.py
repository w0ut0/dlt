import dlt


@dlt.resource(name="users", columns={"email": {"classifiers": ["pii.email"]}})
def resource():
    yield from [{
        "name": "dave",
        "email": "dave@dlthub.com",
    }, {
        "name": "marcin",
        "email": "marcin@dlthub.com",
    },
    {
        "name": "adrian",
        "email": "adrian@dlthub.com"
    }]


p = dlt.pipeline("sdf_test", destination="duckdb")
p.run(resource())

# dlt pipeline sdf_test schema --format sql
# dlt pipeline sdf_test schema --format sdf