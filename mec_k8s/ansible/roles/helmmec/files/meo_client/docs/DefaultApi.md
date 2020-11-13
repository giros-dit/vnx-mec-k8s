# meo_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_app_packages_app_pkgm_v1_app_packages_get**](DefaultApi.md#get_app_packages_app_pkgm_v1_app_packages_get) | **GET** /app_pkgm/v1/app_packages | Get App Packages
[**onboard_app_package_app_pkgm_v1_app_packages_post**](DefaultApi.md#onboard_app_package_app_pkgm_v1_app_packages_post) | **POST** /app_pkgm/v1/app_packages | Onboard App Package


# **get_app_packages_app_pkgm_v1_app_packages_get**
> list[AppPkgInfo] get_app_packages_app_pkgm_v1_app_packages_get(app_d_id=app_d_id)

Get App Packages

### Example

```python
from __future__ import print_function
import time
import meo_client
from meo_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = meo_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with meo_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = meo_client.DefaultApi(api_client)
    app_d_id = 'app_d_id_example' # str |  (optional)

    try:
        # Get App Packages
        api_response = api_instance.get_app_packages_app_pkgm_v1_app_packages_get(app_d_id=app_d_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_app_packages_app_pkgm_v1_app_packages_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_d_id** | **str**|  | [optional] 

### Return type

[**list[AppPkgInfo]**](AppPkgInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **onboard_app_package_app_pkgm_v1_app_packages_post**
> AppPkgInfo onboard_app_package_app_pkgm_v1_app_packages_post(create_app_pkg)

Onboard App Package

### Example

```python
from __future__ import print_function
import time
import meo_client
from meo_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = meo_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with meo_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = meo_client.DefaultApi(api_client)
    create_app_pkg = meo_client.CreateAppPkg() # CreateAppPkg | 

    try:
        # Onboard App Package
        api_response = api_instance.onboard_app_package_app_pkgm_v1_app_packages_post(create_app_pkg)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->onboard_app_package_app_pkgm_v1_app_packages_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_app_pkg** | [**CreateAppPkg**](CreateAppPkg.md)|  | 

### Return type

[**AppPkgInfo**](AppPkgInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

