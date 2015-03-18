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


class InvalidMFAError(RoundError):

    def __init__(self):
        self.message = "Multi-factor authentication failed. Invalid MFA token."


class MFARequiredError(RoundError):

    def __init__(self):
        self.message = "Multi-factor authentication required. Prompt user for to get a token from their TOPT - or if the user hasn't configured TOPT they will have been sent an SMS with the token. Retry this action with the mfa_token= kwarg."


class AuthenticationError(RoundError):

    def __init__(self, context, schemes):
        error_message = u""
        self.valid_schemes = schemes
        for scheme in schemes:
            if scheme in context.schemes:
                error_message += context.schemes[scheme][u'usage'] + "\n"

        self.message = u"You must first authenticate this client with one of:\n{}".format(error_message)
