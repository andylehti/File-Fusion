# File Fusion
## File Merger and File Splitter

This is a Python script for merging multiple text files into one. The resulting file will contain all the lines from the input files, merged together in the order they were read. The script also provides options for checking if the files have the same number of lines and columns, finding differences between the files, splitting a file into groups of characters, and the abillity to split files into various options.

## Requirements

- Python 3.5 or higher

## Usage

1. Clone the repository or download the script file
2. Open a command prompt or terminal window and navigate to the directory where the script is located
3. Run the script using the following command:

   ```python file_merger.py <directory> [-c] [-d] [-f]```

   Replace `<directory>` with the path to the directory containing the text files you want to merge.

   The optional arguments are:

   - `-c` or `--check`: check if all files have the same number of lines, positions, and columns
   - `-d` or `--diffs`: find differences between files
   - `-f` or `--force`: force merge files and ignore errors
   - `-s` or `--split`: split file into identical files but each one only has one character for each file
   - `-q` or `--quit`: quit if using the console GUI

4. Follow the prompts to complete the selected action.

## Examples

To merge all the text files in the directory `/path/to/directory` and check if they have the same number of lines and columns, run:

```
python file_merger.py /path/to/directory -c
```

To merge all the text files in the directory `/path/to/directory` and find differences between them, run:

```
python file_merger.py /path/to/directory -d
```

To merge all the text files in the directory `/path/to/directory` and force merge files even if errors occur, run:

```
python file_merger.py /path/to/directory -f
```

## License

This script is licensed under the MIT License. See the `LICENSE` file for more information.
