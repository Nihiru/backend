#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import hashlib
import config
from config import Configured
from tools import *
from log import Log, err



def check_rights(user, project, right):
    user = user.name
    test = [group for
            group in config.conf["groups"] if check_rights_groups(group, user, project, right)]
    return (len(test) > 0)


def check_rights_groups(group, user, project, right):
    group = Group(group)
    try:
        for p in ["_all", project]:
            if (p in group.projects.keys()):
                for u in ["_all", user]:
                    for r in group.projects[p].keys():
                        try:
                            if (u in group.projects[p][r].keys()):
                                r = Role(r)
                                if r.right[right] == True:
                                    return True
                        except:
                            if (u == group.projects[p][r]):
                                r = Role(r)
                                if r.right[right] == True:
                                    return True
    except:
        config.log.write(err())
    return False


class Group(Configured):

    def __init__(self, name=None):
        Configured.__init__(self, "groups", name)

        try:
            self.projects = self.conf["projects"]
        except:
            self.projects = {}


class User(Configured):

    def __init__(self, name=None):
        Configured.__init__(self, "users", name)

        try:
            self.display_name = self.conf["display_name"]
        except:
            self.display_name = self.name

        try:
            self.password = self.conf["password"]
        except:
            self.password = None

        self.auth = False
        self.active = False
        self.anonymous = False

    def check_password(self, password):
        return (self.password == password)

    def is_authenticated(self):
        return self.auth

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return self.anonymous

    def get_id(self):
        return self.name


class Role(Configured):

    def __init__(self, name=None):
        Configured.__init__(self, "roles", name)

        self.right = {}

        for right in ["create", "read", "update", "delete"]:
            try:
                self.right[right] = self.conf[right]
            except:
                self.right[right] = False
