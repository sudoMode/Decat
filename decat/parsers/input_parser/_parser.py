from argparse import ArgumentParser
# from _config import CLI_CONFIG


def _add_positional_arguments(parser, config):
    if not(isinstance(parser, ArgumentParser)):
        raise TypeError(f'Expected "ArgumentParser" object, received {type(parser)}')
    for name, options in config.items():
        sub_parser = parser.add_subparsers(dest=name)
        _build_command(sub_parser, name=name, **options)


def _add_optional_arguments(parser, config):
    if not(isinstance(parser, ArgumentParser)):
        raise TypeError(f'Expected "ArgumentParser" object, received {type(parser)}')
    for _, options in config.items():
        name, flag = options['name'], options['flag']
        options = {k: v for (k, v) in options.items() if k not in ['name', 'flag']}
        parser.add_argument(name, flag, **options)


# noinspection PyShadowingBuiltins
def _build_command(parser, name=None, help=None, description=None, positional_arguments=None,
                   optional_arguments=None):
    command = parser.add_parser(name, help=help, description=description)
    if optional_arguments is not None:
        _add_optional_arguments(command, optional_arguments)
    if positional_arguments is not None:
        _add_positional_arguments(command, positional_arguments)


def parse_user_args(command_line=None):
    # root parser
    parser = ArgumentParser(prog='decat',
                            description='A Python program that de-concatenates the strings'
                                        'that do not have spaces in them.',
                            )
    parser.add_argument('--input', '-i', dest='input', required=False,
                        type=str, help='Use this argument to specify your input.\n'
                                       'This switch accepts either a piece of text'
                                       'or a valid file path to read text from.'
                        )
    parser.add_argument('--output', '-o', dest='output', type=str, default=None,
                        help='Use this argument to specify an output location,'
                             'by default program would display the output to console.'
                        )
    parser.add_argument('--version', '-V', default=False, action='store_true',
                        help='Display the version of the program')
    args = parser.parse_args(command_line)

    return vars(args)


if __name__ == '__main__':
    # specify test arguments in a list -> (ex: ['run', 'tickers', '-l', '1', '2'])
    command_line = None
    print(f'User Args: {parse_user_args(command_line=command_line)}')
