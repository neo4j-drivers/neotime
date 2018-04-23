#!/usr/bin/env python
# coding: utf-8

# Copyright 2018, Nigel Small & Neo4j
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import division

from neotime import Time
from neotime.clock import Clock


class TimeZone(int):

    __instances = {}

    def __new__(cls, offset):
        instance = cls.__instances.get(offset)
        if instance is None:
            instance = cls.__instances[offset] = int.__new__(TimeZone, offset)
        return instance

    def __repr__(self):
        return "TimeZone(offset=%r)" % int(self)

    @property
    def offset(self):
        return int(self)


UTC = GMT = TimeZone(offset=0)


class ZonedTime(Time):

    __zone = None

    def __new__(cls, hour, minute, second, zone):
        instance = Time.__new__(cls, hour, minute, second)
        instance.__zone = zone
        return instance

    def __repr__(self):
        return "ZonedTime(%r, %r, %r, %r)" % self.hours_minutes_seconds + (self.__zone,)


class LocalTime(ZonedTime):

    def __new__(cls, hour, minute, second):
        return ZonedTime.__new__(cls, hour, minute, second, UTC)  # TODO: find local time zone

    def __repr__(self):
        return "LocalTime(%r, %r, %r)" % self.hours_minutes_seconds


def now(zone=None):
    seconds, nanoseconds = Clock.read_utc()
    return Time.from_unix_time(seconds, nanoseconds)
