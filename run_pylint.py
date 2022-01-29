#!/usr/bin/env python3
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

import re
import sys
import pylint
if __name__ == '__main__':
    version = [int(v) for v in pylint.version.split('.')]
    if version[0] != 2 or version[1] < 9 or version[1] > 10:
        sys.exit("""pylint version {} detected
Please have pylint version 2.9.x or 2.10.x installed.
Use `pip3 install -U pylint` to upgrade.""".format(pylint.version))
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(pylint.run_pylint())
