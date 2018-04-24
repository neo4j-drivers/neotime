================
``neotime.Time``
================

.. class:: Time(hour, minute, second)

.. py:classmethod:: Time.now_utc()

.. py:classmethod:: Date.from_ticks(ticks)


Instance methods and attributes
===============================

.. attribute:: time.ticks

.. attribute:: time.hour

.. attribute:: time.minute

.. attribute:: time.second

.. attribute:: time.hour_minute_second

.. method:: time.replace(hour=0, minute=0, second=0.0)

    Return a :class:`.Time` with one or more components replaced with new values.


Operations
==========

TODO


The :attr:`.Midnight` object
============================

.. attribute:: Midnight

    A :class:`.Time` instance set to `00:00:00`.
    This has a :attr:`ticks <.time.ticks>` value of `0`.
