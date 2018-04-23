# `neotime` -- advanced date/time processing

The `neotime` module provides advanced ISO-8601 compatible date/time functionality with nanosecond precision.

TODO


## Module overview

The `neotime` module defines classes for working with temporal data.
These classes comprise a similar set to that provided by the standard library `datetime` module.
Inspiration has also been drawn from ISO-8601.

The classes are listed below:

* [`Duration`](#duration-objects)
* [`Date`](#date-objects)
* [`Time`](#time-objects)
* TODO

In addition to these classes, the module also exports several constants:

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
--------------|--------------------------------------------------------------
 `months`     | Between -(2<sup>63</sup>) and (2<sup>63</sup> - 1) inclusive
 `days`       | Between -(2<sup>63</sup>) and (2<sup>63</sup> - 1) inclusive
 `seconds`    | Between -(2<sup>63</sup>) and (2<sup>63</sup> - 1) inclusive
 `subseconds` | Between -0.999,999,999 and +0.999,999,999 inclusive

While _seconds_ and _subseconds_ comprise a single logical value, they are stored separately to ensure no loss of precision.
The _seconds_ attribute can hold any value within the signed 64-bit integer range and the _subseconds_ value can be any `float` with a zero before the decimal point.
Both values can be positive or negative but must share the same sign.

Two additional secondary attributes are available, each returning a 3-tuple of derived values.
These are `years_months_days` and `hours_minutes_seconds`.

`Duration` objects support a number of operations. These are listed below.

 Operation       | Result
-----------------|----------------------------
 `d1 + d2`       | A `Duration` representing the sum of `d1` and `d2`.
 `d1 - d2`       | A `Duration` representing the difference between `d1` and `d2`. 
 `d1 * i`        | A `Duration` representing `d1` times `i`, where `i` is an `int`. 
 `d1 * f`        | A `Duration` representing `d1` times `f`, where `f` is a `float`. 
 `d1 / i`        | A `Duration` representing `d1` divided by `i`, where `i` is an `int`. Month and day attributes are rounded to the nearest integer, using round-half-to-even.
 `d1 / f`        | A `Duration` representing `d1` divided by `f`, where `f` is a `float`. Month and day attributes are rounded to the nearest integer, using round-half-to-even.
 `d1 // i`       | A `Duration` representing the floor after `d1` is divided by `i`, where `i` is an `int`.
 `d1 % i`        | A `Duration` representing the remainder after `d1` is divided by `i`, where `i` is an `int`.
 `divmod(d1,i)`  | A pair of `Duration` objects representing the floor and remainder after `d1` is divided by `i`, where `i` is an `int`.
 `+d1`           | A `Duration` identical to `d1`. 
 `-d1`           | A `Duration` that is the inverse of `d1`. Equivalent to `Duration(months=-d1.months, days=-d1.days, seconds=-d1.seconds, subseconds=-d1.subseconds)`. 
 `abs(d1)`       | A `Duration` equal to the absolute value of `d1`. Equivalent to `Duration(months=abs(d1.months), days=abs(d1.days), seconds=abs(d1.seconds), subseconds=abs(d1.subseconds))`. 
 `str(d1)`       | 
 `repr(d1)`      | 
 `bool(d1)`      | `True` if any attribute is non-zero, `False` otherwise. 
 `tuple(d1)`     | A 4-tuple of `(months: int, days: int, seconds: int, subseconds: float)`. 


## ``Date`` objects


## ``Time`` objects
