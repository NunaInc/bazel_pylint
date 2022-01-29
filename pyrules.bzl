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

load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")

def _black_check_test_impl(ctx):
    # add unique name in macro
    exe = ctx.actions.declare_file(ctx.label.name)
    command = "{black_exe} {paths} --check --diff --target-version py37 ".format(
        black_exe = ctx.executable._py_black_shim.short_path,
        paths = " ".join([f.short_path for f in ctx.files.srcs]),
    )
    ctx.actions.write(
        output = exe,
        content = command,
    )
    runfiles = ctx.runfiles(
        files = ctx.files.srcs,
    )
    runfiles = runfiles.merge(
        ctx.attr._py_black_shim[DefaultInfo].default_runfiles,
    )
    return DefaultInfo(
        runfiles = runfiles,
        executable = exe,
    )

black_check_test = rule(
    implementation = _black_check_test_impl,
    test = True,
    attrs = {
        "_py_black_shim": attr.label(
            default = Label("@bazel_pylint//:run_black"),
            executable = True,
            cfg = "host",
        ),
        "srcs": attr.label_list(allow_files = True),
    },
)

def _add_py_check(name, srcs, lint_rules):
    if lint_rules == None:
        lint_rules = "@bazel_pylint//:pylintrc"
    native.genrule(
        name = name + "_pylint",
        srcs = srcs,
        outs = [name + "_pylint.out"],
        tools = [
            "@bazel_pylint//:run_pylint",
            lint_rules,
        ],
        cmd = """
export PYLINTHOME=$$(pwd);
$(location @bazel_pylint//:run_pylint) \
  -sn --rcfile=$(location """ + lint_rules + """) \
  $(SRCS) 2>&1 | tee $@
""",
    )

def _get_lint_rules(attrs):
    lint_rules = attrs.pop("rules", None)
    if not lint_rules:
        return lint_rules
    data = attrs.pop("data", None)
    if data:
        data.append(lint_rules)
    else:
        data = [lint_rules]
    attrs["data"] = data
    return lint_rules

def _check_black(attrs):
    check_black_run = attrs.pop("black_check", None)
    if check_black_run:
        black_check_test(
            name = attrs["name"] + "_black_check_test",
            srcs = attrs["srcs"],
            tags = ["black_check_test"],
        )

def py_lint_library(**attrs):
    """A py_library rule, that has the sources pylint checked.

    See the original py_library for the meaning of attrs.

    Args:
      **attrs: Rule attributes
    """
    _check_black(attrs)
    lint_rules = _get_lint_rules(attrs)
    py_library(**attrs)
    _add_py_check(attrs["name"], attrs["srcs"], lint_rules)

def py_lint_binary(**attrs):
    """A py_binary rule, that has the sources pylint checked.

    See the original py_binary for the meaning of attrs.

    Args:
      **attrs: Rule attributes
    """
    _check_black(attrs)
    lint_rules = _get_lint_rules(attrs)
    py_binary(**attrs)
    _add_py_check(attrs["name"], attrs["srcs"], lint_rules)

def py_lint_test(**attrs):
    """A py_test rule, that has the sources pylint checked.

    See the original py_test for the meaning of attrs.

    Args:
      **attrs: Rule attributes
    """
    _check_black(attrs)
    lint_rules = _get_lint_rules(attrs)
    py_test(**attrs)
    _add_py_check(attrs["name"], attrs["srcs"], lint_rules)
