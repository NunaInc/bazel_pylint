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
"""Example py_lint_binary source."""

import py_library
import py_library2
from typing import NewType

if __name__ == '__main__':
  foo = py_library.Foo(10)
  print(f'add: {foo.add(5)}')
  foo2 = py_library2.Foo(20)
  print(f'add2: {foo2.add(10)}')
  annotated_type = NewType(f'Annotated_{py_library.Foo(10)}', int)
  print(f'Annotated type: {annotated_type}')
