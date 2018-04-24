====================
``neotime.Duration``
====================

A ``Duration`` represents the difference between two points in time.
Duration objects store a composite value of `months`, `days` and `seconds`.
Unlike ``datetime.timedelta`` however, days and seconds are never interchanged
and are applied separately in calculations.

.. class:: Duration(years=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0, subseconds=0, milliseconds=0, microseconds=0, nanoseconds=0)

    All arguments are optional and default to zero.

.. attribute:: Duration.min

    The lowest duration value possible.

.. attribute:: Duration.max

    The highest duration value possible.


Instance methods and attributes
===============================

A ``Duration`` stores four primary instance attributes internally: ``months``, ``days``, ``seconds`` and ``subseconds``.
These are maintained as individual values and are immutable.
Each of these four attributes can carry its own sign, with the exception of ``subseconds``, which must have the same sign as ``seconds``.
This structure allows the modelling of durations such as `3 months minus 2 days`.

Two additional secondary attributes are available, each returning a 3-tuple of derived values.
These are ``years_months_days`` and ``hours_minutes_seconds``.

The primary instance attributes and their permitted ranges are listed below.

==============  ========================================================
Attribute       Value
--------------  --------------------------------------------------------
``months``      Between -(2\ :sup:`63`) and (2\ :sup:`63` - 1) inclusive
``days``        Between -(2\ :sup:`63`) and (2\ :sup:`63` - 1) inclusive
``seconds``     Between -(2\ :sup:`63`) and (2\ :sup:`63` - 1) inclusive
``subseconds``  Between -0.999,999,999 and +0.999,999,999 inclusive
==============  ========================================================


Operations
==========

:class:``.Duration`` objects support a number of operations. These are listed below.

========================  ====================================================================================================================================================================================
Operation                 Result
------------------------  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
``d1 + d2``               A ``Duration`` representing the sum of ``d1`` and ``d2`` .
``d1 - d2``               A ``Duration`` representing the difference between ``d1`` and ``d2`` .
``d1 * i``                A ``Duration`` representing ``d1`` times ``i``, where ``i`` is an ``int``.
``d1 * f``                A ``Duration`` representing ``d1`` times ``f``, where ``f`` is a ``float``.
``d1 / i``                A ``Duration`` representing ``d1`` divided by ``i``, where ``i`` is an ``int``. Month and day attributes are rounded to the nearest integer, using round-half-to-even.
``d1 / f``                A ``Duration`` representing ``d1`` divided by ``f``, where ``f`` is a ``float``. Month and day attributes are rounded to the nearest integer, using round-half-to-even.
``d1 // i``               A ``Duration`` representing the floor after ``d1`` is divided by ``i``, where ``i`` is an ``int``.
``d1 % i``                A ``Duration`` representing the remainder after ``d1`` is divided by ``i``, where ``i`` is an ``int``.
``divmod(d1, i)``         A pair of ``Duration`` objects representing the floor and remainder after ``d1`` is divided by ``i``, where ``i`` is an ``int``.
``+d1``                   A ``Duration`` identical to ``d1`` .
``-d1``                   A ``Duration`` that is the inverse of ``d1``. Equivalent to ``Duration(months=-d1.months, days=-d1.days, seconds=-d1.seconds, subseconds=-d1.subseconds)``.
``abs(d1)``               A ``Duration`` equal to the absolute value of ``d1``. Equivalent to ``Duration(months=abs(d1.months), days=abs(d1.days), seconds=abs(d1.seconds), subseconds=abs(d1.subseconds))``.
``str(d1)``
``repr(d1)``
``bool(d1)``              :const:`True` if any attribute is non-zero, :const:`False` otherwise.
``tuple(d1)``             A 4-tuple of ``(months: int, days: int, seconds: int, subseconds: float)``.
========================  ====================================================================================================================================================================================
