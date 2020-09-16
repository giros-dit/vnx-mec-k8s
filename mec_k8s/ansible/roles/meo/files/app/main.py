from enum import Enum
from fastapi import FastAPI, status, HTTPException
from helm_release_ops import create_release, delete_release
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Optional, List
from bson.objectid import ObjectId


# Initialize MongoDB
client = MongoClient('mongodb://default-mongodb:27017')
db = client.mepm


def preload_helm_releases():
    db.helm_releases.drop()
    db.helm_releases.insert_many(helm_releases)


helm_releases = [
    {
        "appDId": "1",
        "helm_chart": {
            "repository": "https://kubernetes-charts.storage.googleapis.com",
            "name": "grafana",
            "version": "5.1.2"
        }
    }
]
preload_helm_releases()


# MongoDB operations
def get_helm_release(appDId: str):
    helm_release = db.helm_releases.find_one(
                    {'appDId': appDId})
    return helm_release


def delete_app_instance_info(appInstanceId: str):
    app_instance_info = db.app_instances_info.delete_one(
                    {'_id': ObjectId(appInstanceId)})
    return app_instance_info


def get_app_instance_info(appInstanceId: str):
    app_instance_info = db.app_instances_info.find_one(
                    {'_id': ObjectId(appInstanceId)})
    return app_instance_info


def get_app_instances_info():
    app_instances_info = db.app_instances_info.find()
    return app_instances_info


# Definition of Data Models
class CreateAppInstanceRequest(BaseModel):
    appDId: str
    appInstanceName: str
    appInstanceDescription: str


class InstantiateAppRequest(BaseModel):
    virtualComputeDescriptor: Optional[list] = None
    virtualStorageDescriptor: Optional[list] = None
    selectedMECHostInfo: Optional[str] = "Test MEC Host"


class InstantiationState(str, Enum):
    NOT_STANTIATED = "NOT_STANTIATED"
    STANTIATED = "STANTIATED"


class AppInstanceInfo(BaseModel):
    appInstanceId: str
    appInstanceName: str
    appInstanceDescription: str
    appDId: str
    appPkgId: str
    instantiationState: InstantiationState

# FastAPI specific code
app = FastAPI(
    title="MEPM Mm3 AppLcm API",
    description="Implementation of Mm3.AppLcm APIs",
    version="1.0.0")


@app.post("/app_lcm/v1/app_instances", status_code=status.HTTP_201_CREATED)
async def create_app_instance(app_instance_request: CreateAppInstanceRequest):
    app_instance_info = {
        "appInstanceName": app_instance_request.appInstanceName,
        "appInstanceDescription": app_instance_request.appInstanceDescription,
        "appDId": app_instance_request.appDId,
        "appPkgId": app_instance_request.appDId,
        "instantiationState": InstantiationState.NOT_STANTIATED
    }
    app_instance_id = db.app_instances_info.insert_one(
                        app_instance_info).inserted_id

    return {"appInstanceId": "%s" % app_instance_id}


@app.get("/app_lcm/v1/app_instances",
         response_model=List[AppInstanceInfo],
         status_code=status.HTTP_200_OK)
async def get_app_instances():
    app_instances_info = []
    for info in get_app_instances_info():
        info['appInstanceId'] = str(info.pop('_id'))
        app_instances_info.append(info)

    return [AppInstanceInfo(**info) for info in app_instances_info]


@app.delete("/app_lcm/v1/app_instances/{appInstanceId}",
            status_code=status.HTTP_204_NO_CONTENT)
async def delete_app_instance(appInstanceId: str):
    app_instance_info = get_app_instance_info(appInstanceId)
    if app_instance_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="App instance not found")
    if app_instance_info.get('instantiationState') == InstantiationState.STANTIATED.value:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Cannot delete MEC Application instance in 'STANTIATED' state")
    delete_app_instance_info(appInstanceId)


@app.get("/app_lcm/v1/app_instances/{appInstanceId}",
         response_model=AppInstanceInfo,
         status_code=status.HTTP_200_OK)
async def get_app_instance(appInstanceId: str):
    app_instance_info = get_app_instance_info(appInstanceId)
    if app_instance_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="App instance not found")
    app_instance_info['appInstanceId'] = str(app_instance_info.pop('_id'))

    return AppInstanceInfo(**app_instance_info)


@app.post("/app_lcm/v1/app_instances/{appInstanceId}/instantiate",
          status_code=status.HTTP_202_ACCEPTED)
async def instantiate_app_instance(
                appInstanceId: str,
                instantiateAppRequest: InstantiateAppRequest):
    app_instance_info = get_app_instance_info(appInstanceId)
    if app_instance_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="App instance not found")
    if app_instance_info.get('instantiationState') == InstantiationState.STANTIATED.value:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="MEC Application already present")
    appDId = app_instance_info.get('appDId')
    helm_release = get_helm_release(appDId)
    try:
        create_release(
            repository=helm_release['repository'],
            name=helm_release['name'],
            version=helm_release['version'])
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="MEC Application could not be instantiated.")
    db.app_instances_info.update_one(
        {'_id': ObjectId(appInstanceId)},
        {"$set": {"instantiationState": InstantiationState.STANTIATED.value}})


@app.post("/app_lcm/v1/app_instances/{appInstanceId}/terminate",
          status_code=status.HTTP_202_ACCEPTED)
async def terminate_app_instance(
                appInstanceId: str):
    app_instance_info = get_app_instance_info(appInstanceId)
    if app_instance_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="App instance not found")
    if app_instance_info.get('instantiationState') == InstantiationState.NOT_STANTIATED.value:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Cannot terminate MEC Application in 'NOT_STANTIATED' state")
    appDId = app_instance_info.get('appDId')
    helm_release = get_helm_release(appDId)
    try:
        delete_release(name=helm_release['name'])
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="MEC Application could not be instantiated.")
    db.app_instances_info.update_one(
        {'_id': ObjectId(appInstanceId)},
        {"$set": {"instantiationState": InstantiationState.NOT_STANTIATED.value}})