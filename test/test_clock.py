#!/usr/bin/env python
# coding: utf-8

# Copyright 2018, Nigel Small & Neo4j
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from unittest import TestCase

from neotime.clock import T


class TimeSpecTestCase(TestCase):

    def test_zero_timebase(self):
        tb = T()
        self.assertEqual(tb.seconds, 0)
        self.assertEqual(tb.nanoseconds, 0)

    def test_only_seconds(self):
        tb = T(123456)
        self.assertEqual(tb.seconds, 123456)
        self.assertEqual(tb.nanoseconds, 0)

    def test_only_nanoseconds(self):
        tb = T((0, 123456789))
        self.assertEqual(tb.seconds, 0)
        self.assertEqual(tb.nanoseconds, 123456789)

    def test_nanoseconds_overflow(self):
        tb = T((0, 2123456789))
        self.assertEqual(tb.seconds, 2)
        self.assertEqual(tb.nanoseconds, 123456789)

    def test_positive_nanoseconds(self):
        tb = T((1, 1))
        self.assertEqual(tb.seconds, 1)
        self.assertEqual(tb.nanoseconds, 1)

    def test_negative_nanoseconds(self):
        tb = T((1, -1))
        self.assertEqual(tb.seconds, 0)
        self.assertEqual(tb.nanoseconds, 999999999)
