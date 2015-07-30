# -*- coding: utf-8 -*-
# users.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from __future__ import unicode_literals
from past.builtins import basestring

from patchboard.response import ResponseError

from .config import *


class RoundError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    @property
    def msg(self):
        return self.message


class PageError(RoundError, KeyError):
    def __init__(self, i=None):
        self.message = "No page at index: {}".format(i)

class UnknownNetworkError(RoundError):
    def __init__(self, network):
        self.message = (
            "Invalid network: `{}`. Please specify one of our "
            "supported networks: {}").format(network, SUPPORTED_NETWORKS)


class AuthenticationError(RoundError):

    def __init__(self, context, schemes):
        error_message = ""
        if isinstance(schemes, basestring):
            schemes = [schemes]
        self.valid_schemes = schemes
        for scheme in schemes:
            if scheme in context.schemes:
                error_message += context.schemes[scheme]['usage'] + "\n"
        if error_message == "":
            self.message = (
                "The requested action cannot be completed from this "
                "client. You may need to use the Gem Web Console.")
        else:
            self.message = (
                "You must first authenticate this client with one of:\n{}"
            ).format(error_message)

class ConflictError(RoundError):
    pass

class InvalidPassphraseError(RoundError):
    def __init__(self, message="Decryption failed, check your passphrase"):
        self.message = message

class DecryptionError(RoundError):
    def __init__(self, message=("Decryption failed, you may have to update "
                                "your wallet or check your passphrase.")):
        self.message = message

class OverrideError(RoundError):

    def __init__(self, scheme, message=None):
        auth_function = "NOT IMPLEMENTED"
        if scheme == 'Gem-Identify':
            auth_function = 'authenticate_identify'
        elif scheme == 'Gem-Device':
            auth_function = 'authenticate_device'
        elif scheme == 'Gem-Application':
            auth_function = 'authenticate_application'

        super(OverrideError, self).__init__(
            message or ("This client already has {} authentication. To "
                        "overwrite it call {} with override=True.").format(
                            scheme, auth_function))


class AuthUsageError(RoundError):

    def __init__(self, context, scheme):
        self.message = "Usage: {}".format(
            context.schemes[scheme]['usage'])
