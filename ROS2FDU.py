# Copyright (c) 2014,2020 ADLINK Technology Inc.
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0, or the Apache License, Version 2.0
# which is available at https://www.apache.org/licenses/LICENSE-2.0.
#
# SPDX-License-Identifier: EPL-2.0 OR Apache-2.0
#
# Contributors: Gabriele Baldoni, ADLINK Technology Inc. - ROS2 Plugin

import sys
import os
from fog05_sdk.interfaces.States import State
from fog05_sdk.interfaces.InfraFDU import InfraFDU

class ROS2FDU(InfraFDU):
    def __init__(self, data, name, outfile):
        super(ROS2FDU, self).__init__(data)

        self.name = name
        self.app_path = self.image.get('uri')
        self.cmd = None
        self.args = None

        if self.command is not None:
            self.cmd = self.command.get('binary')
            self.args = self.command.get('args')
        else:
            raise ValueError("Command cannot be None for ROS2 application")

        self.outfile = outfile

        self.namespace = None
        self.virtual_interfaces = []
        self.instance_cps = []
        self.pid = -1

    def set_cmd(self, command):
        self.command = command
        if command is not None:
            self.cmd = command.get('binary')
            self.args = command.get('args')

    def set_app_path(self, app_path):
        self.app_path = app_path

    def on_defined(self):
        self.set_status(State.DEFINED)

    def on_configured(self):
        self.set_status(State.CONFIGURED)

    def on_clean(self):
        self.set_status(State.DEFINED)

    def on_start(self, pid):
        self.pid = pid
        self.set_status(State.RUNNING)

    def on_stop(self):
        self.pid = -1
        self.set_status(State.CONFIGURED)

    def on_pause(self):
        self.set_status(State.PAUSED)

    def on_resume(self):
        self.set_status(State.RUNNING)

    def before_migrate(self):
        pass

    def after_migrate(self):
        pass

    def __str__(self):
        s = 'UUID {} Name {} Command {} ARGS {} OUTFILE {} PID {}' \
            ' SOURCE {}'.format(self.uuid, self.name, self.command,
                                self.args, self.outfile, self.pid, self.image)
        return s
