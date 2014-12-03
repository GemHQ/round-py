# -*- coding: utf-8 -*-
# users.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from patchboard.response import ResponseError


class RoundError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    @property
    def msg(self):
        return self.message


class UnknownKeyError(RoundError):

    def __init__(self, key):
        self.key = key
        self.message = "No OTP key found for user. A new key has been generated and a new secret has been delivered. Use key={} to call complete_device_authorization (you should catch this error and use error.key).".format(key)


class OTPConflictError(RoundError):

    def __init__(self):
        self.message = "User has too many outstanding device authorizations."
