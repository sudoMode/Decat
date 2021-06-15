from decat import parse_user_args


def _print_version():
    print('Version..')


def main():
    args = parse_user_args()
    print(f'UA: {args}')


if __name__ == '__main__':
    main()
