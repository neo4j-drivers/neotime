.. currentmodule:: neotime

====================
``neotime.DateTime``
====================

The :class:`.DateTime` class is a nanosecond-precision drop-in replacement for the standard library `datetime <https://docs.python.org/3/library/datetime.html#datetime.datetime>`_ class.
As such, it contains both :class:`.Date` and :class:`.Time` information and draws functionality from those individual classes.
A high degree of API compatibility with the standard library classes is provided.
This includes aliases for method names to allow, for example, :meth:`.DateTime.from_ordinal` to be called as :meth:`.DateTime.fromordinal`.

A :class:`.DateTime` object is fully compatible with the Python time zone library `pytz <http://pytz.sourceforge.net/>`_.
Functions such as `normalize` and `localize` can be used in the same way as they are with the standard library classes.


Constructors and other class methods
====================================

.. autoclass:: DateTime(year, month, day, hour=0, minute=0, second=0.0, tzinfo=None)

.. py:classmethod:: DateTime.now()

.. py:classmethod:: DateTime.utc_now()

.. py:classmethod:: DateTime.from_iso_format(s)

.. py:classmethod:: DateTime.from_timestamp(timestamp, tz=None)

.. py:classmethod:: DateTime.utc_from_timestamp(timestamp)

.. py:classmethod:: DateTime.from_ordinal(ordinal)

.. py:classmethod:: DateTime.combine(date, time)

.. py:classmethod:: DateTime.parse(timestamp, tz=None)

.. py:classmethod:: DateTime.from_native(datetime)

.. py:classmethod:: DateTime.from_clock_time(t, epoch)


Class attributes
================

.. attribute:: DateTime.min

.. attribute:: DateTime.max

.. attribute:: DateTime.resolution


Instance attributes
===================

.. attribute:: dt.year

.. attribute:: dt.month

.. attribute:: dt.day

.. attribute:: dt.year_month_day

.. attribute:: dt.year_week_day

.. attribute:: dt.year_day

.. attribute:: dt.hour

.. attribute:: dt.minute

.. attribute:: dt.second

.. attribute:: dt.tzinfo

.. attribute:: dt.hour_minute_second


Operations
==========

.. describe:: hash(dt)

.. describe:: dt1 == dt2

.. describe:: dt1 != dt2

.. describe:: dt1 < dt2

.. describe:: dt1 > dt2

.. describe:: dt1 <= dt2

.. describe:: dt1 >= dt2

.. describe:: dt1 + timedelta -> dt2
              dt1 + duration -> dt2

.. describe:: dt1 - timedelta -> dt2
              dt1 - duration -> dt2

.. describe:: dt1 - dt2 -> timedelta


Instance methods
================

.. method:: dt.date()

.. method:: dt.time()

.. method:: dt.timetz()

.. method:: dt.replace(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute, second=self.second, tzinfo=self.tzinfo)

    Return a :class:`.DateTime` with one or more components replaced with new values.

.. method:: dt.as_timezone()

.. method:: dt.utc_offset()

.. method:: dt.dst()

.. method:: dt.tzname()

.. method:: dt.time_tuple()

.. method:: dt.utc_time_tuple()

.. method:: dt.to_ordinal()

.. method:: dt.to_native()

    Convert to a native Python :class:`datetime.datetime` value.
    Note that this conversion is potentially lossy, reducing subsecond precision from nanoseconds to microseconds.

.. method:: dt.weekday()

.. method:: dt.iso_weekday()

.. method:: dt.iso_calendar()

.. method:: dt.iso_format()

.. method:: dt.__repr__()

.. method:: dt.__str__()

.. method:: dt.__format__()


Special values
==============

.. attribute:: Never

    A :class:`.DateTime` instance set to `0000-00-00T00:00:00`.
    This has a :class:`.Date` component equal to :attr:`.ZeroDate` and a :class:`.Time` component equal to :attr:`.Midnight`.

.. attribute:: UnixEpoch

    A :class:`.DateTime` instance set to `1970-01-01T00:00:00`.
