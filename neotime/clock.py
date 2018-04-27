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


from __future__ import division, print_function

from ctypes import CDLL, Structure, c_longlong, c_long, byref
from time import gmtime, mktime

from neotime import nano_divmod


MIN_INT64 = -(2 ** 63)
MAX_INT64 = (2 ** 63) - 1


class Clock(object):
    """ An accessor for wall clock time.
    """

    __clock_types = None

    def __new__(cls):
        if cls.__clock_types is None:
            # Find an available clock with the best precision
            cls.__clock_types = sorted((clock for clock in Clock.__subclasses__() if clock.available()),
                                       key=lambda clock: clock.precision(), reverse=True)
        if not cls.__clock_types:
            raise RuntimeError("No clocks available")
        instance = object.__new__(cls.__clock_types[0])
        return instance

    @classmethod
    def precision(cls):
        raise NotImplementedError()

    @classmethod
    def available(cls):
        return False

    @classmethod
    def local_offset(cls):
        return T(-int(mktime(gmtime(0))))

    def local_time(self):
        return self.utc_time() + self.local_offset()

    def utc_time(self):
        raise NotImplementedError()


class SafeClock(Clock):

    @classmethod
    def precision(cls):
        return 6

    @classmethod
    def available(cls):
        return True

    def utc_time(self):
        from time import time
        seconds, nanoseconds = nano_divmod(time() * 1000000000, 1000000000)
        return T((seconds, nanoseconds))


class LibCClock(Clock):

    class _TimeSpec(Structure):
        _fields_ = [
            ("seconds", c_longlong),
            ("nanoseconds", c_long),
        ]

    @classmethod
    def precision(cls):
        return 9

    @classmethod
    def available(cls):
        try:
            _ = CDLL("libc.so.6")
        except OSError:
            return False
        else:
            return True

    def utc_time(self):
        libc = CDLL("libc.so.6")
        ts = self._TimeSpec()
        status = libc.clock_gettime(0, byref(ts))
        if status == 0:
            return T((ts.seconds, ts.nanoseconds))
        else:
            raise RuntimeError("clock_gettime failed with status %d" % status)


class PEP564Clock(Clock):

    @classmethod
    def precision(cls):
        return 9

    @classmethod
    def available(cls):
        try:
            from time import time_ns
        except ImportError:
            return False
        else:
            return True

    def utc_time(self):
        from time import time_ns
        t = time_ns()
        seconds, nanoseconds = divmod(t, 1000000000)
        return T((seconds, nanoseconds))


class T(tuple):
    """ Holds a count of seconds and nanoseconds.
    This can be used to mark a specific point in time, relative to an
    external epoch, or can store an elapsed duration.

    i64, i32
    """

    min = None
    max = None

    def __new__(cls, t=0):
        if hasattr(t, "__neotime_t__"):
            return t.__neotime_t__()
        if isinstance(t, tuple) and len(t) == 2:
            s, ns = map(int, t)
            s, ns = nano_divmod(1000000000 * s + ns, 1000000000)
            return tuple.__new__(cls, (s, ns))
        return tuple.__new__(cls, (int(t), 0))

    def __int__(self):
        return self[0]

    def __float__(self):
        return (1000000000 * self[0] + self[1]) / 1000000000

    def __add__(self, other):
        from neotime import Duration
        if isinstance(other, T):
            return T((self.seconds + other.seconds, self.nanoseconds + other.nanoseconds))
        if isinstance(other, Duration):
            if other.months or other.days:
                raise ValueError("Cannot add Duration with months or days")
            return T((self.seconds + other.seconds, self.nanoseconds + int(other.subseconds * 1000000000)))
        if isinstance(other, float):
            seconds, nanoseconds = divmod(1000000000 * other, 1000000000)
            return T((self.seconds + seconds, self.nanoseconds + nanoseconds))
        if isinstance(other, int):
            return T((self.seconds + other, self.nanoseconds))
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, T):
            return T((self.seconds - other.seconds, self.nanoseconds - other.nanoseconds))
        if isinstance(other, float):
            seconds, nanoseconds = divmod(1000000000 * other, 1000000000)
            return T((self.seconds - seconds, self.nanoseconds - nanoseconds))
        if isinstance(other, int):
            return T((self.seconds - other, self.nanoseconds))
        return NotImplemented

    def __repr__(self):
        return "T(seconds=%r, nanoseconds=%r)" % self

    @property
    def seconds(self):
        return self[0]

    @property
    def nanoseconds(self):
        return self[1]

    @property
    def precision(self):
        return self[2]

T.min = T(0)
T.max = T((MAX_INT64, 999999999))


if __name__ == "__main__":
    print(Clock().utc_time())
