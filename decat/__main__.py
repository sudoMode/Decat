from decat import parse_user_args
from decat import print_version
from decat import decat


def main():
    args = parse_user_args()
    if args.input:
        out = decat(args.input)
        print(out)
    if args.version:
        print_version()


if __name__ == '__main__':
    main()
