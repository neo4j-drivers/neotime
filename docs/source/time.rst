.. currentmodule:: neotime

================
``neotime.Time``
================

The :class:`.Time` class is a nanosecond-precision drop-in replacement for the standard library `time <https://docs.python.org/3/library/datetime.html#datetime.time>`_ class.
A high degree of API compatibility with the standard library classes is provided.
This includes aliases for method names to allow, for example, :meth:`.Time.utc_now` to be called as :meth:`.Time.utcnow`.

:class:`.Time` objects introduce the concept of `ticks`.
This is simply a count of the number of seconds since midnight, in many ways analogous to the :class:`.Date` ordinal.
`Ticks` values can be fractional, with a minimum value of `0` and a maximum of `86399.999999999`.


Constructors and other class methods
====================================

.. class:: Time(hour, minute, second, tzinfo=None)

.. py:classmethod:: Time.now()

.. py:classmethod:: Time.utc_now()

.. py:classmethod:: Time.from_ticks(ticks)

.. py:classmethod:: Time.from_clock_time(t, epoch)


Class attributes
================

.. attribute:: Time.min

.. attribute:: Time.max

.. attribute:: Time.resolution


Instance attributes
===================

.. attribute:: t.ticks

.. attribute:: t.hour

.. attribute:: t.minute

.. attribute:: t.second

.. attribute:: t.hour_minute_second

.. attribute:: t.tzinfo


Operations
==========

.. describe:: hash(t)

.. describe:: t1 == t2

.. describe:: t1 != t2

.. describe:: t1 < t2

.. describe:: t1 > t2

.. describe:: t1 <= t2

.. describe:: t1 >= t2

.. describe:: t1 + timedelta -> t2
              t1 + duration -> t2

.. describe:: t1 - timedelta -> t2
              t1 - duration -> t2

.. describe:: t1 - t2 -> timedelta


Instance methods
================

.. method:: t.replace(hour=self.hour, minute=self.minute, second=self.second, tzinfo=self.tzinfo)

    Return a :class:`.Time` with one or more components replaced with new values.

.. method:: t.utc_offset()

.. method:: t.dst()

.. method:: t.tzname()

.. method:: t.iso_format()

.. method:: t.__repr__()

.. method:: t.__str__()

.. method:: t.__format__()


Special values
==============

.. attribute:: Midnight

    A :class:`.Time` instance set to `00:00:00`.
    This has a :attr:`ticks <.time.ticks>` value of `0`.

.. attribute:: Midday

    A :class:`.Time` instance set to `12:00:00`.
    This has a :attr:`ticks <.time.ticks>` value of `43200`.
