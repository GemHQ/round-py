# -*- coding: utf-8 -*-
# devices.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from __future__ import unicode_literals

from .config import *

from .wrappers import Wrapper
from .errors import *

class Devices(Wrapper):
    """A wrapper class for user.devices.create -- not an actual collection"""

    def create(self, name, redirect_uri=None):
        """Create a new Device object.

        Devices tie Users and Applications together. For your Application to
        access and act on behalf of a User, the User must authorize a Device
        created by your Application.

        This function will return a `device_token` which you must store and use
        after the Device is approved in
          `client.authenticate_device(api_token, device_token)`

        The second value returned is an `mfa_uri` which is the location the User
        must visit to approve the new device. After this function completes,
        you should launch a new browser tab or webview with this value as the
        location. After the User approves the Device, they will be redirected to
        the redirect_uri you specify in this call.

        Args:
          name (str): Human-readable name for the device
            (e.g. "Suzanne's iPhone")
          redirect_uri (str, optional): A URI to which to redirect the User after
            they approve the new Device.

        Returns: A tuple of (device_token, mfa_uri)
        """

        data = dict(name=name)
        if redirect_uri:
            data['redirect_uri'] = redirect_uri

        auth_request_resource = self.resource.create(data)

        return (auth_request_resource.attributes['metadata']['device_token'],
                auth_request_resource.attributes['mfa_uri'])
