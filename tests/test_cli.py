import inspect
import os
import shutil

import wikipron
from wikipron.config import Config
from wikipron.cli import _get_cli_args


_TERMINAL_COMMAND = "wikipron"


def test_terminal_command():
    assert shutil.which(_TERMINAL_COMMAND), (
        f'The terminal command "{_TERMINAL_COMMAND}" does not exist. '
        "Is the package not installed correctly? "
        f'Or is the command "{_TERMINAL_COMMAND}" not defined in setup.py?'
    )
    smoke_test_command = f"{_TERMINAL_COMMAND} --help"
    help_manual = os.popen(smoke_test_command).read()
    assert wikipron.__doc__ in help_manual, (
        f'The command "{_TERMINAL_COMMAND}" exists but does not work. '
        f'The smoke test with "{smoke_test_command}" may have diagnostic '
        "information to stderr."
    )


def test_cli_args_match_config_args():
    config_args = inspect.getfullargspec(Config.__init__)
    cli_args = _get_cli_args(["eng"])
    assert cli_args.__dict__ == {
        **config_args.kwonlydefaults,
        "key": "eng",
    }, "CLI and Config.__init__ must have the same args and their defaults."
