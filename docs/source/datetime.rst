====================
``neotime.DateTime``
====================

.. class:: DateTime(year, month, day, hour, minute, second)

.. py:classmethod:: DateTime.now_utc()

.. py:classmethod:: DateTime.from_ticks(ticks)


Instance methods and attributes
===============================

.. attribute:: date_time.date

.. attribute:: date_time.year

.. attribute:: date_time.month

.. attribute:: date_time.day

.. attribute:: date_time.year_month_day

.. attribute:: date_time.year_week_day

.. attribute:: date_time.year_day

.. attribute:: date_time.time

.. attribute:: date_time.hour

.. attribute:: date_time.minute

.. attribute:: date_time.second

.. attribute:: date_time.hour_minute_second

.. method:: date_time.replace(year=0, month=0, day=0, hour=0, minute=0, second=0.0)

    Return a :class:`.DateTime` with one or more components replaced with new values.


Operations
==========

TODO


The :attr:`.Never` object
=========================

.. attribute:: Never

    A :class:`.DateTime` instance set to `0000-00-00T00:00:00`.
    This has a :attr:`ticks <.time.ticks>` value of `0`.
