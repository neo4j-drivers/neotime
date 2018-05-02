.. module:: neotime

===================================================
``neotime`` -- Nanosecond resolution temporal types
===================================================

The ``neotime`` module defines classes for working with temporal data to nanosecond precision.
These classes comprise a similar set to that provided by the standard library ``datetime`` module.

.. toctree::
    :maxdepth: 2
    :caption: Classes:

    clocktime
    clock
    duration
    date
    time
    datetime

In addition to these classes, the module exports several constants:

.. attribute:: neotime.MIN_YEAR

    The smallest year number available.
    ``MIN_YEAR`` equals `1`.

.. attribute:: neotime.MAX_YEAR

    The largest year number available.
    ``MAX_YEAR`` equals `9999`.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
