.. currentmodule:: neotime

=================
``neotime.Clock``
=================

Accessor for time values. This class is fulfilled by implementations
that subclass :class:`.Clock`. These implementations are contained within
the ``neotime.clock_implementations`` module, and are not intended to be
accessed directly.

Creating a new :class:`.Clock` instance will produce the highest
precision clock implementation available.

    >>> clock = Clock()
    >>> type(clock)
    neotime.clock_implementations.LibCClock
    >>> clock.local_time()
    ClockTime(seconds=1525265942, nanoseconds=506844026)


Constructor
===========

.. class:: Clock()

    Construct and return a new :class:`.Clock` object using the best
    implementation available.


Class attributes
================

.. attribute:: Clock.precision()

    The precision of this clock implementation, represented as a
    number of decimal places. Therefore, for a nanosecond precision
    clock, this function returns `9`.

.. attribute:: Clock.local_offset()

    The offset from UTC for local time read from this clock.


Instance methods
================

.. method:: c.local_time()

    Read and return the current local time from this clock, measured
    relative to the Unix Epoch.

.. method:: c.utc_time()

    Read and return the current UTC time from this clock, measured
    relative to the Unix Epoch.
