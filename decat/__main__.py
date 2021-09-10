from parsers import parse_user_args
from core import decat


def _print_version():
    from __settings__ import VERSION
    print(f'Decat {VERSION}')


def main():
    args = parse_user_args()
    if args.input:
        out = decat(args.input)
        print(out)
        return out
    if args.version:
        _print_version()


if __name__ == '__main__':
    main()
