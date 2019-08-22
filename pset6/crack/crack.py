import sys

def main() -> int:
    if len(sys.argv) == 2:
        hash = sys.argv[1]
        salt = hash[:2]

        crack(hash, salt)
    else:
        print("Invalid arguments")
        return 1;

    return 0;


def crack(hash, salt):
    print(f"{hash}, {salt}\ncracked");


if __name__ == '__main__':
    main()