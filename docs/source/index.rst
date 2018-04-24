.. module:: neotime

=======================================================
``neotime`` -- Temporal types with nanosecond precision
=======================================================

The ``neotime`` module defines classes for working with temporal data.
These classes comprise a similar set to that provided by the standard library ``datetime`` module.
Inspiration has also been drawn from `ISO-8601 <https://xkcd.com/1179/>`_.

.. toctree::
    :maxdepth: 2
    :caption: Classes:

    duration
    date
    time

In addition to these classes, the module also exports several constants:

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
