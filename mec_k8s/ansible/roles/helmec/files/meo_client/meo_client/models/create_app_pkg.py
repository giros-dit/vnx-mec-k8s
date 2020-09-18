# coding: utf-8

"""
    MEO Mm1 AppPkgMgmt API

    Implementation of Mm1.AppPkgm APIs  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from meo_client.configuration import Configuration


class CreateAppPkg(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'app_pkg_name': 'str',
        'app_pkg_version': 'str',
        'app_provider': 'str',
        'user_defined_data': 'object',
        'app_pkg_path': 'str'
    }

    attribute_map = {
        'app_pkg_name': 'appPkgName',
        'app_pkg_version': 'appPkgVersion',
        'app_provider': 'appProvider',
        'user_defined_data': 'userDefinedData',
        'app_pkg_path': 'appPkgPath'
    }

    def __init__(self, app_pkg_name=None, app_pkg_version=None, app_provider=None, user_defined_data=None, app_pkg_path=None, local_vars_configuration=None):  # noqa: E501
        """CreateAppPkg - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._app_pkg_name = None
        self._app_pkg_version = None
        self._app_provider = None
        self._user_defined_data = None
        self._app_pkg_path = None
        self.discriminator = None

        self.app_pkg_name = app_pkg_name
        self.app_pkg_version = app_pkg_version
        self.app_provider = app_provider
        if user_defined_data is not None:
            self.user_defined_data = user_defined_data
        self.app_pkg_path = app_pkg_path

    @property
    def app_pkg_name(self):
        """Gets the app_pkg_name of this CreateAppPkg.  # noqa: E501


        :return: The app_pkg_name of this CreateAppPkg.  # noqa: E501
        :rtype: str
        """
        return self._app_pkg_name

    @app_pkg_name.setter
    def app_pkg_name(self, app_pkg_name):
        """Sets the app_pkg_name of this CreateAppPkg.


        :param app_pkg_name: The app_pkg_name of this CreateAppPkg.  # noqa: E501
        :type app_pkg_name: str
        """
        if self.local_vars_configuration.client_side_validation and app_pkg_name is None:  # noqa: E501
            raise ValueError("Invalid value for `app_pkg_name`, must not be `None`")  # noqa: E501

        self._app_pkg_name = app_pkg_name

    @property
    def app_pkg_version(self):
        """Gets the app_pkg_version of this CreateAppPkg.  # noqa: E501


        :return: The app_pkg_version of this CreateAppPkg.  # noqa: E501
        :rtype: str
        """
        return self._app_pkg_version

    @app_pkg_version.setter
    def app_pkg_version(self, app_pkg_version):
        """Sets the app_pkg_version of this CreateAppPkg.


        :param app_pkg_version: The app_pkg_version of this CreateAppPkg.  # noqa: E501
        :type app_pkg_version: str
        """
        if self.local_vars_configuration.client_side_validation and app_pkg_version is None:  # noqa: E501
            raise ValueError("Invalid value for `app_pkg_version`, must not be `None`")  # noqa: E501

        self._app_pkg_version = app_pkg_version

    @property
    def app_provider(self):
        """Gets the app_provider of this CreateAppPkg.  # noqa: E501


        :return: The app_provider of this CreateAppPkg.  # noqa: E501
        :rtype: str
        """
        return self._app_provider

    @app_provider.setter
    def app_provider(self, app_provider):
        """Sets the app_provider of this CreateAppPkg.


        :param app_provider: The app_provider of this CreateAppPkg.  # noqa: E501
        :type app_provider: str
        """
        if self.local_vars_configuration.client_side_validation and app_provider is None:  # noqa: E501
            raise ValueError("Invalid value for `app_provider`, must not be `None`")  # noqa: E501

        self._app_provider = app_provider

    @property
    def user_defined_data(self):
        """Gets the user_defined_data of this CreateAppPkg.  # noqa: E501


        :return: The user_defined_data of this CreateAppPkg.  # noqa: E501
        :rtype: object
        """
        return self._user_defined_data

    @user_defined_data.setter
    def user_defined_data(self, user_defined_data):
        """Sets the user_defined_data of this CreateAppPkg.


        :param user_defined_data: The user_defined_data of this CreateAppPkg.  # noqa: E501
        :type user_defined_data: object
        """

        self._user_defined_data = user_defined_data

    @property
    def app_pkg_path(self):
        """Gets the app_pkg_path of this CreateAppPkg.  # noqa: E501


        :return: The app_pkg_path of this CreateAppPkg.  # noqa: E501
        :rtype: str
        """
        return self._app_pkg_path

    @app_pkg_path.setter
    def app_pkg_path(self, app_pkg_path):
        """Sets the app_pkg_path of this CreateAppPkg.


        :param app_pkg_path: The app_pkg_path of this CreateAppPkg.  # noqa: E501
        :type app_pkg_path: str
        """
        if self.local_vars_configuration.client_side_validation and app_pkg_path is None:  # noqa: E501
            raise ValueError("Invalid value for `app_pkg_path`, must not be `None`")  # noqa: E501

        self._app_pkg_path = app_pkg_path

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CreateAppPkg):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateAppPkg):
            return True

        return self.to_dict() != other.to_dict()
