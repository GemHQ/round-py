# -*- coding: utf-8 -*-
# users.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from patchboard.response import ResponseError
from config import *


class RoundError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    @property
    def msg(self):
        return self.message


class UnknownNetworkError(RoundError):
    def __init__(self, network):
        self.message = "Invalid network: `{}`. Please specify one of our supported networks: {}".format(network, SUPPORTED_NETWORKS)


class UnknownKeyError(RoundError):

    def __init__(self, key):
        self.key = key
        self.message = "No OTP key found for user. A new key has been generated and a new secret has been delivered. Use key={} to call complete_device_authorization (you should catch this error and use error.key).".format(key)


class AuthenticationError(RoundError):

    def __init__(self, context, schemes):
        error_message = u""
        if isinstance(schemes, basestring):
            schemes = [schemes]
        self.valid_schemes = schemes
        for scheme in schemes:
            if scheme in context.schemes:
                error_message += context.schemes[scheme][u'usage'] + "\n"
        if error_message == u"":
            self.message = u"The requested action cannot be completed from this client. You may need to use the Gem User or Developer Console."
        else:
            self.message = u"You must first authenticate this client with one of:\n{}".format(error_message)

class ConflictError(RoundError):
    pass

class OverrideError(RoundError):

    def __init__(self, scheme, message=None):
        auth_function = "NOT IMPLEMENTED"
        if scheme == u'Gem-Identify':
            auth_function = 'authenticate_identify'
        elif scheme == u'Gem-Device':
            auth_function = 'authenticate_device'
        elif scheme == u'Gem-Application':
            auth_function = 'authenticate_application'

        super(OverrideError, self).__init__(message or u"This client already has {} authentication. To overwrite it call {} with override=True.".format(scheme, auth_function))




class AuthUsageError(RoundError):

    def __init__(self, context, scheme):
        self.message = u"Usage: {}".format(
            context.schemes[scheme][u'usage'])
