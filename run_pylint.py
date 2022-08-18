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
import subprocess
import sys

if __name__ == '__main__':
    # Note: pylint has GPL 2.0 license - but we invoked it as an external program,
    #       not as an included library, and this artefact does not include any
    #       portion of the pylint library, and is no derivation of the pylint work.
    result = subprocess.run([sys.executable, '-m', 'pylint', '--version'],
                            capture_output=True,
                            check=True)
    version_str = result.stdout.decode('utf-8').split('\n')[0].split(' ')[1]
    version = [int(v) for v in version_str.split('.')]
    if version[0] != 2 or version[1] < 9 or version[1] > 14:
        sys.exit("""pylint version {} detected
Please have pylint version 2.9.x or 2.14.x installed.
Use `pip3 install -U pylint` to upgrade.""".format(version))
    args = [sys.executable, '-m', 'pylint']
    args.extend(sys.argv[1:])
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)
