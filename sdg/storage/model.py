from pydantic import BaseModel

class Driver(BaseModel):
    endpoint: str
    available_space: int
    used_space: int
    total_space: int

class BucketInfo(BaseModel):
    type: str
    value: int


class Metric(BaseModel):
    objects: int
    online_drivers: int
    offline_drivers: int
    drivers: list[Driver]
    buckets: list[BucketInfo]