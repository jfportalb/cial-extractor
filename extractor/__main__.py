import fileinput

def main():
    for line in fileinput.input():
        line = line.rstrip()
        print(line)


if __name__ == "__main__":
    main()
