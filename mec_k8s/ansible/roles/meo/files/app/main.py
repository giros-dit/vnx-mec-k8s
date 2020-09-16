from enum import Enum
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Optional, List
from bson.objectid import ObjectId


# Initialize MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client.meo

# MongoDB operations
def get_app_packages_info(appDId):
    filter = None
    if appDId:
        filter = {'_id': ObjectId(appDId)}
    app_pkgs_info = db.app_pkgs_info.find(filter=filter)
    return app_pkgs_info


# Definition of Data Models
class CreateAppPkg(BaseModel):
    appPkgName: str
    appPkgVersion: str
    appProvider: str
    userDefinedData: Optional[dict]
    appPkgPath: str


class OnboardingState(str, Enum):
    CREATED = "CREATED"
    UPLOADING = "UPLOADING"
    PROCESSING = "PROCESSING"
    ONBOARDED = "ONBOARDED"


class OperationalState(str, Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class UsageState(str, Enum):
    IN_USE = "IN_USE"
    NOT_IN_USE = "NOT_IN_USE"


class AppPkgInfo(BaseModel):
    appPkgId: str
    appDId: str
    appProvider: str
    appName: str
    softwareImages: dict
    onboardingState: OnboardingState
    operationalState: OperationalState
    usageState: UsageState
    userDefinedData: Optional[dict]

# FastAPI specific code
app = FastAPI(
    title="MEO Mm1 AppPkgMgmt API",
    description="Implementation of Mm1.AppPkgm APIs",
    version="1.0.0")


@app.post("/app_pkgm/v1/app_packages",
          response_model=AppPkgInfo,
          status_code=status.HTTP_201_CREATED)
async def onboard_app_package(createAppPkg: CreateAppPkg):
    app_pkg_info = {
        "appProvider": createAppPkg.appProvider,
        "appName": createAppPkg.appPkgName,
        "softwareImages": {
            "repository": createAppPkg.appPkgPath,
            "name": createAppPkg.appPkgName,
            "version": createAppPkg.appPkgVersion
        },
        "onboardingState": OnboardingState.ONBOARDED.value,
        "operationalState": OperationalState.ENABLED.value,
        "usageState": UsageState.NOT_IN_USE.value,
        "userDefinedData": createAppPkg.userDefinedData
    }

    app_pkg_id = db.app_pkgs_info.insert_one(
                    app_pkg_info).inserted_id
    
    return AppPkgInfo(
        appPkgId=str(app_pkg_id),
        appDId=str(app_pkg_id),
        **app_pkg_info
    )

@app.get("/app_pkgm/v1/app_packages", response_model=List[AppPkgInfo],
         status_code=status.HTTP_200_OK)
async def get_app_packages(appDId: Optional[str] = None):
    app_pkgs_info = []
    for info in get_app_packages_info(appDId):
        info['appPkgId'] = str(info['_id'])
        info['appDId'] = info['appPkgId']
        app_pkgs_info.append(info)

    return [AppPkgInfo(**info) for info in app_pkgs_info]
