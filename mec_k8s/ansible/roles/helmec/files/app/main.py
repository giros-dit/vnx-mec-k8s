from enum import Enum
from fastapi import FastAPI, status, HTTPException
from helm_release_ops import create_release, delete_release
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List
from bson.objectid import ObjectId

import meo_client
from meo_client.rest import ApiException

MEO_ADDRESS = "10.10.20.10"

# Initialize MongoDB
client = MongoClient('mongodb://default-mongodb:27017')
db = client.mepm


# MongoDB operations
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


def get_helm_release(appDId: str):
    # Defining the host is optional and defaults to http://localhost
    # See configuration.py for a list of all supported configuration parameters.
    configuration = meo_client.Configuration(host="http://%s" % MEO_ADDRESS)

    # Enter a context with an instance of the API client
    with meo_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = meo_client.DefaultApi(api_client)
        try:
            # Get App Package
            api_response = api_instance.get_app_packages_app_pkgm_v1_app_packages_get(app_d_id=appDId)
            return api_response[0]
        except ApiException as e:
            print("Exception when calling DefaultApi->get_app_packages_app_pkgm_v1_app_packages_get: %s\n" % e)


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
                appInstanceId: str):
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
            repository=helm_release.software_images['repository'],
            name=helm_release.software_images['name'],
            version=helm_release.software_images['version'],
            values=helm_release.user_defined_data)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="MEC Application could not be instantiated.")
    else:
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
        delete_release(name=helm_release.app_name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="MEC Application could not be instantiated.")
    else:
        db.app_instances_info.update_one(
            {'_id': ObjectId(appInstanceId)},
            {"$set": {"instantiationState": InstantiationState.NOT_STANTIATED.value}})