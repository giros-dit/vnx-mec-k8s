from kubernetes import client, config

def create_release(repository, name, version):
    config.load_incluster_config()

    group = "helm.fluxcd.io"
    api_version = "v1"
    plural = "helmreleases"
    namespace = "default"
    api_instance = client.CustomObjectsApi()

    helmrelease = {
        "apiVersion": "helm.fluxcd.io/v1",
        "kind": "HelmRelease",
        "metadata": {
            "name": name,
            "namespace": "default"
        },
        "spec": {
            "chart": {
                "repository": repository,
                "name": name,
                "version": version
            },
            "wait": True
        }
    }

    api_response = api_instance.create_namespaced_custom_object(
        group=group,
        version=api_version,
        plural=plural,
        namespace=namespace,
        body=helmrelease,
    )

    return api_response


def list_releases():
    config.load_incluster_config()

    group = "helm.fluxcd.io"
    version = "v1"
    plural = "helmreleases"
    api_instance = client.CustomObjectsApi()

    api_response = api_instance.list_cluster_custom_object(
        group=group,
        version=version,
        plural=plural)

    return api_response


def delete_release(name):
    config.load_incluster_config()

    group = "helm.fluxcd.io"
    api_version = "v1"
    plural = "helmreleases"
    namespace = "default"
    api_instance = client.CustomObjectsApi()

    api_response = api_instance.delete_namespaced_custom_object(
        group=group,
        version=api_version,
        plural=plural,
        namespace=namespace,
        name=name)

    return api_response
