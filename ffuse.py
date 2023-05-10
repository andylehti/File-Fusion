import os
import sys
import argparse

def get_file_list(directory):
    file_list = [file for file in os.listdir(directory) if file.endswith(".txt") and not file.startswith("//")]
    with open("list.txt", "w") as list_file:
        for file in file_list:
            list_file.write(file + "\n")
    return file_list


def read_file_content(file_path):
    with open(file_path, "r") as file:
        return file.readlines()

def check_files(directory, file_list):
    files_ok = True
    master_lines = read_file_content(os.path.join(directory, file_list[0]))
    for file in file_list[1:]:
        lines = read_file_content(os.path.join(directory, file))
        if len(lines) != len(master_lines):
            print(f"File {file} does not have the same number of lines as the other files.")
            files_ok = False
            continue
        for i, line in enumerate(lines):
            if len(line) != len(master_lines[i]):
                print(f"File {file} does not have the same number of positions or columns as the other files on line {i + 1}.")
                files_ok = False
                break
    return files_ok

def find_diffs(directory, file_list):
    master_lines = read_file_content(os.path.join(directory, file_list[0]))
    for file in file_list[1:]:
        lines = read_file_content(os.path.join(directory, file))
        for i, line in enumerate(lines):
            for j, char in enumerate(line.rstrip('\n')):
                if char != ' ' and j < len(master_lines[i]) and master_lines[i][j] != ' ' and master_lines[i][j] != char:
                    print(f"Conflict in file {file}, line {i + 1}, position {j + 1}")

def merge_files(directory, file_list, force_merge=False):
    master_lines = []

    for file in file_list:
        file_path = os.path.join(directory, file)
        lines = read_file_content(file_path)

        if not master_lines:
            master_lines = lines
        else:
            max_lines = max(len(master_lines), len(lines))
            for index in range(max_lines):
                if index >= len(master_lines):
                    master_lines.append(lines[index])
                elif index >= len(lines):
                    break
                else:
                    if len(lines[index]) > len(master_lines[index]):
                        master_lines[index] = master_lines[index].rstrip() + ' ' * (len(lines[index]) - len(master_lines[index])) + '\n'

    rejected = 0

    for file in file_list:
        file_path = os.path.join(directory, file)
        lines = read_file_content(file_path)

        for i, line in enumerate(lines):
            for j, char in enumerate(line.rstrip('\n')):
                if char != ' ' and (i >= len(master_lines) or j >= len(master_lines[i].rstrip('\n')) or master_lines[i][j] == ' '):
                    try:
                        master_lines[i] = master_lines[i][:j] + char + master_lines[i][j+1:]
                    except IndexError:
                        master_lines[i] = master_lines[i][:j] + char + '\n'
                elif char != ' ' and master_lines[i][j] != char:
                    print(f"Conflict in file {file}, line {i + 1}, position {j + 1}")
                    rejected += 1
                    if not force_merge:
                        sys.exit(1)

    with open("master.txt", "w") as master_file:
        for line in master_lines:
            master_file.write(line)

    print(f"Rejected characters: {rejected}")

def split_file(directory, input_file, mode):
    with open(os.path.join(directory, input_file), "r") as file:
        content = file.read()

    if mode == "alphabetic":
        groups = [chr(i) for i in range(ord('a'), ord('z') + 1)] + ["other"]
        regex_list = [re.compile(f'[^{c}\n]', re.IGNORECASE) for c in groups[:-1]] + [re.compile(r'[a-z]', re.IGNORECASE)]
    elif mode == "case_alphabetic":
        groups = [chr(i) for i in range(ord('a'), ord('z') + 1)] + [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ["other"]
        regex_list = [re.compile(f'[^{c}\n]') for c in groups[:-1]] + [re.compile(r'[a-zA-Z]')]
    elif mode == "alphanumeric":
        groups = [chr(i) for i in range(ord('a'), ord('z') + 1)] + [chr(i) for i in range(ord('A'), ord('Z') + 1)] + [str(i) for i in range(10)] + ["other"]
        regex_list = [re.compile(f'[^{c}\n]') for c in groups[:-1]] + [re.compile(r'[a-zA-Z0-9]')]
    else:
        print("Invalid mode selected.")
        return

    for group, regex in zip(groups, regex_list):
        split_content = regex.sub(' ', content)
        with open(os.path.join(directory, f"{input_file}_split_{group}.txt"), "w") as split_file:
            split_file.write(split_content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="The directory containing the files to merge.")
    parser.add_argument("-c", "--check", action="store_true", help="Check if all files have the same number of lines, positions, and columns.")
    parser.add_argument("-d", "--diffs", action="store_true", help="Find differences between files.")
    parser.add_argument("-f", "--force", action="store_true", help="Force merge files and ignore errors.")
    args = parser.parse_args()

    file_list = get_file_list(args.directory)

    if args.check:
        files_ok = check_files(args.directory, file_list)
        if not files_ok:
            sys.exit(1)

    if args.diffs:
        find_diffs(args.directory, file_list)

    merge_files(args.directory, file_list, force_merge=args.force)

def main():
    directory = input("Enter the directory path: ")

    while True:
        action = input("Choose an option (-c, -d, -f, -m, -s, -q): ")

        if action == '-c':
            file_list = get_file_list(directory)
            files_ok = check_files(directory, file_list)
            if not files_ok:
                sys.exit(1)
        elif action == '-d':
            file_list = get_file_list(directory)
            find_diffs(directory, file_list)
        elif action == '-f':
            file_list = get_file_list(directory)
            merge_files(directory, file_list, force_merge=True)
        elif action == '-m':
            file_list = get_file_list(directory)
            merge_files(directory, file_list)
        elif action == '-s':
            input_file = input("Enter the input file name: ")
            mode = input("Enter the mode (alphabetic, case_alphabetic, alphanumeric): ")
            split_file(directory, input_file, mode)
        elif action == '-q':
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
