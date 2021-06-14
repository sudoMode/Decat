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
    sub_parser = parser.add_subparsers()
    input_ = sub_parser.add_parser('input')
    input_.add_argument('--string', '-s', dest='input')
    input_.add_argument('--file', '-f', dest='input')
    output = sub_parser.add_parser('output')
    output.add_argument('--string', '-s', dest='output')
    output.add_argument('--file', '-f', dest='output')

    # for name, config in CLI_CONFIG.items():
    #     _build_command(parser, name=name, **config)
    args = parser.parse_args(command_line)

    return vars(args)


if __name__ == '__main__':
    # specify test arguments in a list -> (ex: ['run', 'tickers', '-l', '1', '2'])
    command_line = None
    print(f'User Args: {parse_user_args(command_line=command_line)}')
