from argparse import ArgumentParser
from ._validators import VALIDATORS


input_type = VALIDATORS.get('input', str)


def _validate_user_args(args, parser):
    args_in_a_dict = vars(args)
    values = list(args_in_a_dict.values())
    user_did_not_pass_any_arguments = values.count(None) == len(values)
    if user_did_not_pass_any_arguments:
        parser.print_help()
        exit(0)


def parse_user_args(command_line=None):
    # root parser
    parser = ArgumentParser(prog='decat',
                            description='A Python program that de-concatenates the strings'
                                        'that do not have spaces in them.',
                            )
    parser.add_argument('--input', '-i', dest='input', required=False,
                        type=input_type, help='Use this argument to specify your input.\n'
                                       'This switch accepts either a piece of text'
                                       'or a valid file path to read text from.'
                        )
    # parser.add_argument('--output', '-o', dest='output', type=output_type,
    #                     default=None,
    #                     help='Use this argument to specify an output'
    #                          'location, by default program would display'
    #                          'the output to console.'
    #                     )
    parser.add_argument('--version', '-V', default=None, action='store_true',
                        help='Display the version of the program')
    args = parser.parse_args(command_line)
    _validate_user_args(args, parser)
    return args


if __name__ == '__main__':
    # specify test arguments in a list -> (ex: ['run', 'tickers', '-l', '1', '2'])
    command_line = None
    print(f'User Args: {parse_user_args(command_line=command_line)}')
