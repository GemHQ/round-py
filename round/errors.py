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


class OTPConflictError(RoundError):

    def __init__(self):
        self.message = "User does not exist or has too many outstanding device authorizations."


class AuthenticationError(RoundError):

    def __init__(self, context, schemes):
        error_message = u""
        self.valid_schemes = schemes
        for scheme in schemes:
            if scheme in context.schemes:
                error_message += context.schemes[scheme][u'usage'] + "\n"

        self.message = u"You must first authenticate this client with one of:\n{}".format(error_message)
