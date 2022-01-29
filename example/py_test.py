#
# bazel_pylint: Copyright 2022 Nuna Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Example py_lint_test source."""

import unittest
import py_library

class FooTest(unittest.TestCase):

  def test_add_default(self):
    foo = py_library.Foo()
    self.assertEqual(foo.add(10), 11)

  def test_add(self):
    foo = py_library.Foo(5)
    self.assertEqual(foo.add(10), 15)


if __name__ == '__main__':
  unittest.main()
