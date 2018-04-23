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


""" This module contains the fundamental types used for temporal accounting as well as
a number of utility functions.
"""


from neotime.arithmetic import nano_add, nano_sub, nano_mul, nano_div, nano_mod, symmetric_divmod
from neotime.clock import MIN_INT64, MAX_INT64


__version__ = "1.0.0a1"


MIN_YEAR = 1
MAX_YEAR = 9999


class Duration(tuple):
    """ A :class:`.Duration` object...

    i64:i64:i64:i32
    """

    min = None
    max = None

    def __new__(cls, years=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0,
                subseconds=0, milliseconds=0, microseconds=0, nanoseconds=0):
        mo = int(12 * years + months)
        if mo < MIN_INT64 or mo > MAX_INT64:
            raise ValueError("Month out of range")
        d = int(7 * weeks + days)
        if d < MIN_INT64 or d > MAX_INT64:
            raise ValueError("Day out of range")
        s = (int(3600000000000 * hours) +
             int(60000000000 * minutes) +
             int(1000000000 * seconds) +
             int(1000000000 * subseconds) +
             int(1000000 * milliseconds) +
             int(1000 * microseconds) +
             int(nanoseconds))
        s, ss = symmetric_divmod(s, 1000000000)
        if s < MIN_INT64 or s > MAX_INT64:
            raise ValueError("Seconds out of range")
        return tuple.__new__(cls, (mo, d, s, ss / 1000000000))

    def __bool__(self):
        return any(map(bool, self))

    __nonzero__ = __bool__

    def __add__(self, other):
        if not isinstance(other, Duration):
            return NotImplemented
        return Duration(months=self[0] + int(other[0]), days=self[1] + int(other[1]),
                        seconds=self[2] + int(other[2]), subseconds=nano_add(self[3], other[3]))

    def __sub__(self, other):
        if not isinstance(other, Duration):
            return NotImplemented
        return Duration(months=self[0] - int(other[0]), days=self[1] - int(other[1]),
                        seconds=self[2] - int(other[2]), subseconds=nano_sub(self[3], other[3]))

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            return NotImplemented
        return Duration(months=self[0] * other, days=self[1] * other,
                        seconds=self[2] * other, subseconds=nano_mul(self[3], other))

    def __floordiv__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return Duration(months=int(self[0] // other), days=int(self[1] // other),
                        seconds=int(nano_add(self[2], self[3]) // other), subseconds=0)

    def __mod__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return Duration(months=round(self[0] % other), days=round(self[1] % other),
                        seconds=round(self[2] % other), subseconds=nano_mod(self[3], other))

    def __divmod__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return self.__floordiv__(other), self.__mod__(other)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            return NotImplemented
        return Duration(months=round(float(self[0]) / other), days=round(float(self[1]) / other),
                        seconds=float(self[2]) / other, subseconds=nano_div(self[3], other))

    __div__ = __truediv__

    def __pos__(self):
        return self

    def __neg__(self):
        return Duration(months=-self[0], days=-self[1], seconds=-self[2], subseconds=-self[3])

    def __abs__(self):
        return Duration(months=abs(self[0]), days=abs(self[1]), seconds=abs(self[2]), subseconds=abs(self[3]))

    def __repr__(self):
        return "Duration(months=%r, days=%r, seconds=%r, subseconds=%r)" % self

    def __str__(self):
        terms = []
        if self[0]:
            terms.append("%+dmo" % self[0])
        if self[1]:
            terms.append("%+dd" % self[1])
        if self[2] or self[3]:
            s = ("%d" if self[2] == 0 else "%+d") % self[2]
            s += ("%.9f" % abs(self[3])).strip("0")
            if s.endswith("."):
                s += "0"
            terms.append("%ss" % s)
        return " ".join(terms)

    def iso_format(self):
        """

        :return:
        """
        years, months, days = self.years_months_days
        hours, minutes, seconds = self.hours_minutes_seconds
        return "P%04d-%02d-%02dT%02d:%02d:%012.9f" % (years, months, days, hours, minutes, seconds)

    @property
    def months(self):
        """

        :return:
        """
        return self[0]

    @property
    def days(self):
        """

        :return:
        """
        return self[1]

    @property
    def seconds(self):
        """

        :return:
        """
        return self[2]

    @property
    def subseconds(self):
        """

        :return:
        """
        return self[3]

    @property
    def years_months_days(self):
        """

        :return:
        """
        years, months = symmetric_divmod(self[0], 12)
        return years, months, self[1]

    @property
    def hours_minutes_seconds(self):
        """ A 3-tuple of (hours, minutes, seconds).
        """
        minutes, seconds = symmetric_divmod(self[2], 60)
        hours, minutes = symmetric_divmod(minutes, 60)
        return hours, minutes, float(seconds) + self[3]


Duration.min = Duration(months=MIN_INT64, days=MIN_INT64, seconds=MIN_INT64, subseconds=-0.999999999)
Duration.max = Duration(months=MAX_INT64, days=MAX_INT64, seconds=MAX_INT64, subseconds=+0.999999999)


class Date(object):

    min = None
    max = None

    __ordinal = 0
    __year = 0
    __month = 0
    # Holds a value between 1 and 28 or between -1 and -28. Positive values
    # represent days from the 1st to the 28th of the month inclusive and
    # negative values from the last to the 28th from last. This is with the
    # exception of 28-day months, where the last day is always -1.
    #
    # Therefore, for a 31-day month, days 1..28 are generally stored as-is,
    # whereas days 29, 30 and 31 are stored as -3, -2 and -1 respectively.
    # Day values of -4 to -28 are also valid and would also represent real
    # days 28 back to 4. This encoding improves some temporal arithmetic,
    # specifically adding and subtracting months; Adding one month to 31 Oct
    # (month=10, day=-1) gives 30 Nov (month=11, day=-1), adding another
    # month "remembers" the original day, giving 31 Dec (month=12, day=-1).
    #
    #    1   2   3   4   5   6   7             25  26  27  28  29  30  31
    #    |---|---|---|---|---|---| - - - - - - |---|---|---|---|---|---|
    #    1   2   3   4   5   6   7             25  26  27  28
    #               -28 -27 -26 -25           -7  -6  -5  -4  -3  -2  -1
    #
    __day = 0

    #: The smallest possible difference between non-equal :class:`.Date` objects, ``Duration(days=1)``.
    resolution = None

    @classmethod
    def __normalize_year(cls, year):
        if MIN_YEAR <= year <= MAX_YEAR:
            return int(year)
        raise ValueError("Year out of range (%d..%d)" % (MIN_YEAR, MAX_YEAR))

    @classmethod
    def __normalize_month(cls, year, month):
        year = cls.__normalize_year(year)
        if 1 <= month <= 12:
            return year, int(month)
        raise ValueError("Month out of range (1..12)")

    @classmethod
    def __normalize_day(cls, year, month, day):
        """ Coerce the day of the month to an internal value that may or
        may not match the "public" value.

        All days from the 1st to the 27th of the month are stored as-is,
        i.e. 1..27. The last day of the month (28th, 29th, 20th or 31st)
        is always -1, regardless of the length of the month. The remaining
        days are mapped to a value that depends on the number of days in
        that month.

        For a 28-day month, the last week is as follows:

            Day   | 22 23 24 25 26 27 28
            Value | 22 23 24 25 26 27 -1

        For a 29-day month, the last week is as follows:

            Day   | 23 24 25 26 27 28 29
            Value | 23 24 25 26 27 28 -1

        For a 30-day month, the last week is as follows:

            Day   | 24 25 26 27 28 29 30
            Value | 24 25 26 27 28 -2 -1

        For a 31-day month, the last week is as follows:

            Day   | 25 26 27 28 29 30 31
            Value | 25 26 27 28 -3 -2 -1

        This slightly unintuitive system makes some temporal arithmetic
        produce a more desirable outcome.

        :param year:
        :param month:
        :param day:
        :return:
        """
        year, month = cls.__normalize_month(year, month)
        if 1 <= day <= 27 or day == -1:
            return year, month, int(day)
        days_in_month = cls.days_in_month(year, month)
        if day == days_in_month:
            return year, month, -1
        if day == 28:
            return year, month, 28
        if days_in_month == 30:
            if day in (29, -2):
                return year, month, -2
        if days_in_month == 31:
            if day in (30, -2):
                return year, month, -2
            if day in (29, -3):
                return year, month, -3
        # TODO improve this error message
        raise ValueError("Day %d out of range (-28..-1, 1..%d)" % (day, days_in_month))

    @classmethod
    def is_leap_year(cls, year):
        year = cls.__normalize_year(year)
        if year % 4 != 0:
            return False
        if year % 100 != 0:
            return True
        return year % 400 == 0

    @classmethod
    def days_in_year(cls, year):
        return 366 if cls.is_leap_year(year) else 365

    @classmethod
    def days_in_month(cls, year, month):
        year, month = cls.__normalize_month(year, month)
        if month in (9, 4, 6, 11):
            return 30
        elif month != 2:
            return 31
        else:
            return 29 if cls.is_leap_year(year) else 28

    @classmethod
    def from_ordinal(cls, ordinal):
        """ Return the :class:`.Date` that corresponds to the proleptic
        Gregorian ordinal, where ``0001-01-01`` has ordinal 1 and
        ``9999-12-31`` has ordinal 3,652,059. Values outside of this
        range trigger a :exc:`ValueError`. The corresponding instance
        method for the reverse date-to-ordinal transformation is
        :meth:`.to_ordinal`.
        """
        day = int(ordinal)
        if day < 1 or day > 3652059:
            # Note: this requires a maximum of 22 bits for storage
            # Could be transferred in 3 bytes.
            raise ValueError("Ordinal out of range (1..3652059)")
        year = 1
        month = 1
        days_in_year = cls.days_in_year(year)
        while day > days_in_year:
            day -= days_in_year
            year += 1
            days_in_year = cls.days_in_year(year)
        days_in_month = cls.days_in_month(year, month)
        while day > days_in_month:
            day -= days_in_month
            month += 1
            days_in_month = cls.days_in_month(year, month)
        year, month, day = cls.__normalize_day(year, month, day)
        return cls.__new(ordinal, year, month, day)

    @classmethod
    def __new(cls, ordinal, year, month, day):
        instance = object.__new__(cls)
        instance.__ordinal = ordinal
        instance.__year = year
        instance.__month = month
        instance.__day = day
        return instance

    @classmethod
    def __calc_ordinal(cls, year, month, day):
        if day >= 1:
            ordinal = int(day)
        else:
            ordinal = cls.days_in_month(year, month) + int(day) + 1
        for m in range(1, month):
            ordinal += cls.days_in_month(year, m)
        for y in range(1, year):
            ordinal += cls.days_in_year(y)
        return ordinal

    def __new__(cls, year, month, day):
        if year == month == day == 0:
            return object.__new__(cls)
        year, month, day = cls.__normalize_day(year, month, day)
        ordinal = cls.__calc_ordinal(year, month, day)
        return cls.__new(ordinal, year, month, day)

    def __eq__(self, other):
        if isinstance(other, Date):
            return self.ordinal == other.ordinal
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.ordinal)

    def __int__(self):
        return int(self.ordinal)

    def __increment_months(self, months):
        years, months = symmetric_divmod(months, 12)
        year = self.__year + years
        month = self.__month + months
        if month > 12:
            year += 1
            month -= 12
        if month < 1:
            year -= 1
            month -= 12
        self.__year = year
        self.__month = month

    def __increment_days(self, days):
        assert 1 <= self.__day <= 28 or -28 <= self.__day <= -1
        if self.__day >= 1:
            new_days = self.__day + days
            if 1 <= new_days <= 27:
                self.__day = new_days
                return
        new_date = Date.from_ordinal(self.__ordinal + days)
        self.__year, self.__month, self.__day = new_date.__year, new_date.__month, new_date.__day

    def __add__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                return self
            new_date = self.replace()
            Date.__increment_days(new_date, other)
            new_date.__ordinal = self.__calc_ordinal(new_date.year, new_date.month, new_date.day)
            return new_date
        if isinstance(other, Duration):
            if other.seconds or other.subseconds:
                raise ValueError("Cannot add a Duration with seconds or subseconds to a Date")
            if other.months == other.days == 0:
                return self
            new_date = self.replace()
            # Add days before months as the former sometimes
            # requires the current ordinal to be correct.
            if other.days:
                Date.__increment_days(new_date, other.days)
            if other.months:
                Date.__increment_months(new_date, other.months)
            new_date.__ordinal = self.__calc_ordinal(new_date.year, new_date.month, new_date.day)
            return new_date
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Date):
            return Duration(days=(self.ordinal - other.ordinal))
        try:
            return self.__add__(-other)
        except TypeError:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Date):
            return self.ordinal < other.ordinal
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Date):
            return self.ordinal > other.ordinal
        return NotImplemented

    def __repr__(self):
        if self.__ordinal == 0:
            return "Never"
        return "Date(%r, %r, %r)" % self.year_month_day

    def __str__(self):
        if self.__ordinal == 0:
            return "0000-00-00"
        return "%04d-%02d-%02d" % self.year_month_day

    @property
    def ordinal(self):
        """ Return the current value as an ordinal.
        """
        return self.__ordinal

    @property
    def year(self):
        return self.__year

    @property
    def month(self):
        return self.__month

    @property
    def day(self):
        if self.__day == 0:
            return 0
        if self.__day >= 1:
            return self.__day
        return self.days_in_month(self.__year, self.__month) + self.__day + 1

    @property
    def year_month_day(self):
        return self.year, self.month, self.day

    @property
    def year_week_day(self):
        ordinal = self.__ordinal
        year = self.__year

        def day_of_week(o):
            return ((o - 1) % 7) + 1

        def iso_week_1(y):
            j4 = Date(y, 1, 4)
            return j4 + Duration(days=(1 - day_of_week(j4.ordinal)))

        if ordinal >= Date(year, 12, 29).ordinal:
            week1 = iso_week_1(year + 1)
            if ordinal < week1.ordinal:
                week1 = iso_week_1(year)
            else:
                year += 1
        else:
            week1 = iso_week_1(year)
            if ordinal < week1.ordinal:
                year -= 1
                week1 = iso_week_1(year)
        return year, ((ordinal - week1.ordinal) / 7 + 1), day_of_week(ordinal)

    @property
    def year_day(self):
        return self.__year, self.ordinal - Date(self.__year, 1, 1).ordinal + 1

    def replace(self, year=0, month=0, day=0):
        """ Return a :class:`.Date` with one or more components replaced
        with new values.
        """
        return Date(year or self.__year, month or self.__month, day or self.__day)

    def to_struct_time(self):
        raise NotImplementedError()


Date.min = Date.from_ordinal(1)
Date.max = Date.from_ordinal(3652059)
Date.resolution = Duration(days=1)

ZeroDate = Date(0, 0, 0)


class Time(float):
    """ Holds any value between 0 and 86399.999999999 that represents number of seconds since midnight.
    Floats (double precision) are guaranteed to store 15 significant digits without loss, which is all we need.
    """

    @classmethod
    def check_ticks(cls, ticks):
        if ticks < 0 or ticks >= 86400:
            raise ValueError("Ticks out of range (0..86400)")

    @classmethod
    def check_hour(cls, hour):
        if hour < 0 or hour > 23:
            raise ValueError("Hour out of range (0..23)")

    @classmethod
    def check_minute(cls, hour, minute):
        cls.check_hour(hour)
        if minute < 0 or minute > 59:
            raise ValueError("Minute out of range (0..59)")

    @classmethod
    def check_second(cls, hour, minute, second):
        cls.check_minute(hour, minute)
        if second < 0 or second > 59:
            raise ValueError("Second out of range (0..59)")

    @classmethod
    def ticks(cls, hour, minute, second):
        cls.check_second(hour, minute, second)
        return 3600 * hour + 60 * minute + second

    @classmethod
    def hour_minute_second(cls, ticks):
        pass  # TODO

    @classmethod
    def from_unix_time(cls, seconds=None, nanoseconds=None):   # TODO: zone
        from time import gmtime  # TODO rewrite
        utc = gmtime(seconds)
        print((utc.tm_hour, utc.tm_min, utc.tm_sec, nanoseconds))
        return cls(utc.tm_hour, utc.tm_min, utc.tm_sec + float(nanoseconds) / 1000000000)

    @classmethod
    def from_ticks(cls, ticks):
        cls.check_ticks(ticks)
        return super(Time, cls).__new__(cls, ticks)

    def __repr__(self):
        return "Time(%r, %r, %r)" % self.hours_minutes_seconds


Midnight = float.__new__(Time, 0)
