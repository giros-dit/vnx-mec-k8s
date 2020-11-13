docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \                                                                                  
-i  /local/openapi.json \
-g python \
-o /local/ \
--additional-properties=projectName=meo-client \
--additional-properties=packageName=meo_client
