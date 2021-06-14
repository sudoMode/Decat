from decat import parse_user_args


def main():
    user_args = parse_user_args()
    print(f'UA: {user_args}')


if __name__ == '__main__':
    main()
