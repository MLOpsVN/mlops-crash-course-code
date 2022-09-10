from feast import Entity

driver = Entity(
    name="driver",
    join_keys=["driver_id"],
    description="driver id",
    tags={},
    owner="mlopsvn@gmail.com",
)
