import sys

# for x in sys.argv:
#     print(x)

def usage():
    print("Usage: aide.py [OPTION]... [FILE]...")
    sys.exit(-1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
    if sys.argv[1] == "--nb":
        try:
            nb = int(sys.argv[2])
        except ValueError:
            usage()
        else:
            print(nb)