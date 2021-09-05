from decat import parse_user_args


def _print_version():
    from .__settings__ import VERSION
    print(f'Decat {VERSION}')


def main():
    args = parse_user_args()
    if args.input:
        pass  # call decat
    if args.version:
        _print_version()


if __name__ == '__main__':
    main()
