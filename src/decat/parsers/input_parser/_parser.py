from argparse import ArgumentParser

from decat.core.parallel import DEFAULT_EXECUTOR, EXECUTORS
from decat.parsers.input_parser._loaders import LOADERS, load_from_file
from decat.parsers.input_parser._validators import VALIDATORS

input_type = VALIDATORS.get("input", str)


def _validate_user_args(args, parser):
    user_did_not_pass_any_arguments = (
        args.version is False
        and args.input is None
        and args.preserve_special_chars is False
    )
    if user_did_not_pass_any_arguments:
        parser.print_help()
        exit(0)


def parse_user_args(command_line=None):
    # root parser
    parser = ArgumentParser(
        prog="decat",
        description="A Python program that de-concatenates the "
        "strings that do not have white-spaces in them.\n"
        'Example: "testtext" --> ["test", "text"]',
    )
    parser.add_argument(
        "--input",
        "-i",
        dest="input",
        required=False,
        nargs="+",
        type=input_type,
        default=None,
        help="Use this argument to specify one, or multiple input "
        'strings. When used along with "--file-type", this '
        "argument is expected to be one, or multiple paths to "
        "file(s) holding the input strings instead.",
    )
    parser.add_argument(
        "--file-type",
        "-f",
        dest="file_type",
        required=False,
        choices=list(LOADERS.keys()),
        default=None,
        help='Use this argument to indicate that "--input" holds '
        "path(s) to file(s) of the given type, instead of raw "
        "input strings.",
    )
    parser.add_argument(
        "--threads",
        "-t",
        dest="threads",
        required=False,
        type=int,
        default=None,
        help="Number of worker threads/processes to use while "
        "processing multiple inputs concurrently, defaults to "
        "a sensible value picked by the underlying executor.",
    )
    parser.add_argument(
        "--executor",
        "-e",
        dest="executor",
        required=False,
        choices=list(EXECUTORS.keys()),
        default=DEFAULT_EXECUTOR,
        help="Concurrency backend used while processing multiple "
        'inputs, "thread" (default) or "process".',
    )
    parser.add_argument(
        "--version",
        "-v",
        default=False,
        action="store_true",
        help="Display the current version of the program.",
    )
    parser.add_argument(
        "--preserve-special-chars",
        "-p",
        default=False,
        action="store_true",
        help="Use this toggle to preserve punctuation marks & other "
        "special characters in text.",
    )
    args = parser.parse_args(command_line)
    _validate_user_args(args, parser)
    return args


def load_inputs(args):
    """
    Resolves the final input(s) to be processed by decat based on the
    parsed CLI arguments.

    - When "--file-type" is provided, "--input" is treated as one, or
      multiple, file paths from which the input strings are loaded.
    - When a single, raw input string is provided (and no file is
      used), it is returned as-is preserving the original/simple CLI
      behaviour i.e. a flat list of tokens gets printed out.
    - When multiple raw input strings are provided, a list of strings
      is returned so that they get processed concurrently and the
      richer, dictionary based response gets printed out instead.
    """
    if args.file_type:
        return load_from_file(args.input, args.file_type)
    if len(args.input) == 1:
        return args.input[0]
    return args.input


if __name__ == "__main__":
    command_line = None
    print(f"User Args: {parse_user_args(command_line=command_line)}")
