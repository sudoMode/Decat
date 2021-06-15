from decat import parse_user_args


def _print_version():
    print('Version..')


def main():
    args = parse_user_args()

    if args['version']:
        _print_version()


if __name__ == '__main__':
    main()
