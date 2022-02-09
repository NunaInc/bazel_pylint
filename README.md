# bazel_pylint

Bazel components for pylint-ing python build targets.

Offers `py_lint_library`, `py_lint_binary`, `py_lint_test`, which have
the Python sources linted during build process, and correspond in turn
to  `py_libray`, `py_binary` and `py_test`.
This package uses the `rules_python` set of rules, as a subdependency.
You need to have `pip3 install pylint==2.10.2` as a binary on your
machine.


## Setup

### Setup Via `html_archive`:

In your Bazel `WORKSPACE` add a referece to a release of this project:

```python
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
  name = "bazel_pylint",
  urls = ["<url to release archive>"],
  sha256 = "<sha256 of the archive file>",
  strip_prefix = "bazel_pylint-<version>",
)
```

### Setup Via Submodule (alternate)

1/ add the `bazel_pylint` as a git submodule, and initialize it,
say under a `external` directory:

```sh
mkdir external; cd external
git submodule add <git_url>
```

2/ Add the submodule to your Bazel `WORKSPACE` file, and initialize:

```python
new_local_repository(
  name = "bazel_pylint",
  path = "external/bazel_pylint",
  workspace_file = "external/bazel_pylint/WORKSPACE",
  build_file = "external/bazel_pylint/BUILD.bazel",
)
```

### Initialization

Follow one of the set of steps above, with the initialization of
the `bazel_pylint` dependencies in your Bazel `WORKSPACE` file:

```
load("@bazel_pylint//:load.bzl", "bazel_pylint_load_workspace")
bazel_pylint_load_workspace()

load("@bazel_pylint//:setup.bzl", "bazel_pylint_setup_workspace")
bazel_pylint_setup_workspace()
```

## Usage

In your `BUILD` files, you can use the `py_lint_xxx` rules as you
would use the original `py_xxx` rules for `rules_python`:

```python
load("@bazel_pylint//:pyrules.bzl", "py_lint_library")

py_lint_library(
  name = "my_library",
  srcs = ["my_library .py"],
  srcs_version = "PY3",
)
```

## Extra options:

You can pass these extra arguments to the `py_lint_xxx` rules:

* use the `rules = '<rules file target>'` to specify the pylint
rules to use for checking (if not specified it uses the `pylintrc`
from this directory);

* use `check_black = True` to enable a check that the input
source files are formatted according to the
[Black](https://black.readthedocs.io/en/stable/) code formatter
rules.
