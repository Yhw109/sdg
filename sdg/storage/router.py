from fastapi import APIRouter
import requests
from ..config import settings
from .model import BucketInfo, Driver, Metric

router = APIRouter(
    prefix="/storage",
    tags=["storage"],
)

@router.get("/metric", response_model=Metric)
async def get_metric():
    cookie = requests.post(
        url=settings.MINIO_ENDPOINT + "/api/v1/login",
        json={
        "accessKey": settings.MINIO_USERNAME,
        "secretKey": settings.MINIO_PASSWORD
        }
    ).cookies
    response = requests.get(
        url=settings.MINIO_ENDPOINT + "/api/v1/admin/info",
        cookies=cookie
    ).json()
    objects = response["objects"]
    online_drivers = 0
    offline_drivers = 0
    drivers: list[Driver] = []
    for driver in response['servers'][0]['drives']:
        drivers.append(Driver(
            endpoint=driver['endpoint'], 
            available_space=driver['availableSpace'], 
            used_space=driver['usedSpace'], 
            total_space=driver['totalSpace']))
        if driver['state'] == 'ok':
            online_drivers += 1
        else:
            offline_drivers += 1
    response = requests.get(
        url=settings.MINIO_ENDPOINT + "/api/v1/buckets",
        cookies=cookie
    ).json()
    buckets: list[BucketInfo] = []
    for bucket in response['buckets']:
        buckets.append(BucketInfo(type=bucket['name'], value=bucket.get('objects', 0)))
    return Metric(
        objects=objects, 
        online_drivers=online_drivers, 
        offline_drivers=offline_drivers, 
        drivers=drivers, 
        buckets=buckets)
    