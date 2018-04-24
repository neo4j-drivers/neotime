================
``neotime.Date``
================

A :class:`.Date` object represents a date in the `proleptic Gregorian Calendar <https://en.wikipedia.org/wiki/Proleptic_Gregorian_calendar>`_.
Years between `0001` and `9999` are supported, with additional support for the `zero date` used in some contexts.

Each date is based on a proleptic Gregorian ordinal, which models 1 Jan 0001 as `day 1` and counts each subsequent day up to, and including, 31 Dec 9999.
The standard `year`, `month` and `day` value of each date is also available.

Internally, the day of the month is always stored as-is, with the exception of the last three days of that month.
These are always stored as -1, -2 and -3 (counting from the last day).
This system allows some temporal arithmetic (particularly adding or subtracting months) to produce a more desirable outcome than would otherwise be produced.
Externally, the day number is always the same as would be written on a calendar.

.. class:: Date(year, month, day)

    Construct a new :class:`.Date` object.
    All arguments are required and should be integers.
    For general dates, the following ranges are supported:

    =========  ========================  ===================================
    Argument   Minimum                   Maximum
    ---------  ------------------------  -----------------------------------
    ``year``   :attr:`.MIN_YEAR` (0001)  :attr:`.MAX_YEAR` (9999)
    ``month``  1                         12
    ``day``    1                         :attr:`Date.days_in_month(year, month) <Date.days_in_month>`
    =========  ========================  ===================================

    A zero date can also be acquired by passing all zeroes to the :class:`.Date` constructor or by using :attr:`.ZeroDate` directly.

.. py:classmethod:: Date.today_utc()

    Return the current :class:`.Date` according to UTC.

.. py:classmethod:: Date.from_ordinal(ordinal)

    Construct and return a :class:`.Date` from a proleptic Gregorian ordinal.
    This is simply an integer value that corresponds to a day, starting with `1` for 1 Jan 0001.

.. py:classmethod:: Date.is_leap_year(year)

    Return a `bool` value that indicates whether or not `year` is a leap year.

.. py:classmethod:: Date.days_in_year(year)

    Return the number of days in `year`.

.. py:classmethod:: Date.days_in_month(year, month)

    Return the number of days in `month` of `year`.


Instance methods and attributes
===============================

.. attribute:: date.ordinal

.. attribute:: date.year

.. attribute:: date.month

.. attribute:: date.day

.. attribute:: date.year_month_day

.. attribute:: date.year_week_day

.. attribute:: date.year_day

    Return a 2-tuple of year and day number.
    This is the number of the day relative to the start of the year, with `1 Jan` corresponding to `1`.

.. method:: date.replace(year=0, month=0, day=0)

    Return a :class:`.Date` with one or more components replaced with new values.


Operations
==========

TODO


The :attr:`.ZeroDate` object
============================

.. attribute:: ZeroDate

    A :class:`.Date` instance set to `0000-00-00`.
    This has an :attr:`ordinal <.date.ordinal>` value of `0`.
