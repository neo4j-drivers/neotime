# `neotime` -- advanced date/time processing

The `neotime` module provides advanced ISO-8601 compatible date/time functionality with nanosecond precision.

TODO


## Type overview

#### class `neotime.Duration`
> TODO

#### class `neotime.Date`
> TODO

####  class `neotime.Time`
> TODO

In addition, the `neotime` module exports the following constants:

#### `neotime.MIN_YEAR`
> The smallest year number available.
> `MIN_YEAR` equals `1`.

#### `neotime.MAX_YEAR`
> The largest year number available.
> `MAX_YEAR` equals `9999`.


## `Duration` objects
A `Duration` represents the difference between two points in time.
Duration objects store a composite value of _months_, _days_ and _seconds_.
Unlike `datetime.timedelta` however, days and seconds are never interchanged
and are applied separately in calculations.

#### class `neotime.Duration(years=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0, subseconds=0, milliseconds=0, microseconds=0, nanoseconds=0)`
> All arguments are optional and default to zero.

#### `Duration.min`
> The most negative `Duration` possible.

#### `Duration.max`
> The most positive `Duration` possible.

A `Duration` stores four primary instance attributes internally.
As a `Duration` is immutable, these are all read-only.
Each of these four attributes can carry its own sign, with the exception of `subseconds`, which must have the same sign as `seconds`.
This structure allows the modelling of durations such as _3 months minus 2 days_.

The primary instance attributes and their permitted ranges are listed below.

Attribute    | Value
--------------------
`months`     | Between -(2<sup>63</sup>) and (2<sup>63</sup> - 1) inclusive
`days`       | Between -(2<sup>63</sup>) and (2<sup>63</sup> - 1) inclusive
`seconds`    | Between -(2<sup>63</sup>) and (2<sup>63</sup> - 1) inclusive
`subseconds` | Between -0.999,999,999 and +0.999,999,999 inclusive

Two additional secondary attributes are available, each returning a 3-tuple of derived values.
These are `years_months_days` and `hours_minutes_seconds`.


## ``Date`` objects


## ``Time`` objects
