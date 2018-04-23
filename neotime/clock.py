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


from ctypes import CDLL, Structure, c_longlong, c_long, byref


MIN_INT64 = -(2 ** 63)
MAX_INT64 = (2 ** 63) - 1


def _instant_safe():
    from time import time
    seconds, nanoseconds = divmod(time() * 1000000000, 1000000000)
    return Instant(seconds, nanoseconds)


try:

    from time import time_ns as _time_ns

except ImportError:

    try:
        _libc = CDLL("libc.so.6")
    except OSError:
        _instant = _instant_safe
    else:
        def _instant_function():

            time_t = c_longlong

            class CTimeSpec(Structure):
                _fields_ = [
                    ("seconds", time_t),
                    ("nanoseconds", c_long),
                ]

            def f():
                ts = CTimeSpec()
                if _libc.clock_gettime(0, byref(ts)) == 0:
                    return Instant(ts.seconds, ts.nanoseconds)
                else:
                    return _instant_safe()

            return f

        _instant = _instant_function()

else:

    def _instant():
        t = _time_ns()
        seconds, nanoseconds = divmod(t, 1000000000)
        return Instant(seconds, nanoseconds)


class Instant(tuple):
    """ Represents an absolute time, relative to an externally known epoch.

    i64, i32
    """

    min = None
    max = None

    def __new__(cls, seconds=0, nanoseconds=0):
        if seconds < 0 or nanoseconds < 0:
            raise ValueError("Neither seconds nor nanoseconds can be negative")
        seconds, nanoseconds = divmod((1000000000 * seconds + nanoseconds), 1000000000)
        return tuple.__new__(cls, (int(seconds), int(nanoseconds)))

    def __int__(self):
        return self[0]

    def __float__(self):
        return (1000000000 * self[0] + self[1]) / 1000000000

    def __add__(self, other):
        from neotime import Duration
        cls = self.__class__
        if isinstance(other, Instant):
            return cls(self.seconds + other.seconds, self.nanoseconds + other.nanoseconds)
        if isinstance(other, Duration):
            if other.months or other.days:
                raise ValueError("Cannot add Duration with months or days")
            return cls(self.seconds + other.seconds, self.nanoseconds + int(other.subseconds * 1000000000))
        if isinstance(other, float):
            seconds, nanoseconds = divmod(1000000000 * other, 1000000000)
            return cls(self.seconds + seconds, self.nanoseconds + nanoseconds)
        if isinstance(other, int):
            return cls(self.seconds + other, self.nanoseconds)
        return NotImplemented

    def __sub__(self, other):
        try:
            cls = self.__class__
            if isinstance(other, float):
                seconds, nanoseconds = divmod(1000000000 * other, 1000000000)
                return cls(self.seconds - seconds, self.nanoseconds - nanoseconds)
            if isinstance(other, int):
                return cls(self.seconds - other, self.nanoseconds)
            return NotImplemented
        except ValueError:
            raise OverflowError()

    def __repr__(self):
        return "Instant(seconds=%r, nanoseconds=%r)" % self

    @property
    def seconds(self):
        return self[0]

    @property
    def nanoseconds(self):
        return self[1]

Instant.min = Instant(seconds=0, nanoseconds=0)
Instant.max = Instant(seconds=MAX_INT64, nanoseconds=999999999)


class Clock(object):

    @classmethod
    def read_utc(cls):
        return _instant()
