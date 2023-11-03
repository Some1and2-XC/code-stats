#!/usr/bin/env python3

"""
Author : Mark T
Date : 11/2/2023

A python file written purely out of spite for getting all the
python files I've written and getting stats about them

Uses First command line argument to specify the directory
to run the script in. This is an optional argument.
Ex:
    python main.py ../..
"""


from os import walk, path
from sys import argv
import codecs


class file_type_filter:
    def __init__(self, language, keywords=[]):
        self.language = language
        self.keywords = [[keyword, 0] for keyword in keywords]
        self.file_count = 0
        self.line_count = 0

    def add_file(self):
        self.file_count += 1

    def get_filters(self, input_str: str) -> bool:

        # Adds one to line count
        self.line_count += 1

        # Initializes Input Value
        kw_check = input_str.strip()

        # Checks all object filters for value
        for i, (filter_value, _) in enumerate(self.keywords):
            # Adds space to each filter to ensure it is a keyword
            # Also checks if the line is the value as lines such as python
            # 'continue' generally don't have a space afterwards
            if kw_check.startswith(filter_value + " ") or \
                    kw_check == filter_value or \
                    kw_check == filter_value + ":" or \
                    kw_check.startswith(filter_value + "("):
                self.keywords[i][1] += 1
                return True
        return False

    def get_summary(self) -> str:
        """
        Prints the amount of instances for all the filters
        """

        temp_keywords = [[num, kw] for kw, num in self.keywords]
        temp_keywords.sort(reverse=True)

        out_str = f"Language: *{self.language} ({self.file_count} files @ {self.line_count} lines)\n"
        out_str += "\n".join(f"\t{num}\t{kw}" for num, kw in temp_keywords)
        return out_str


# Hack to Ignore File Read Errors
def strict_handler(exception):
    """
    Custom Error Overide Function for ignoring read errors
    """
    print(out_list[i])
    return u"", exception.end


codecs.register_error("strict", strict_handler)

# initializes variables
out_list = []
book_list = []
sum_of_lines = 0

# Sets Path to search via CLI
if len(argv) <= 1:
    path_to_files = "."
else:
    path_to_files = argv[1]

# Sets Filters to use
python_filters = file_type_filter(language=".py", keywords=[
    "try",
    "except",
    "continue",
    "break",
    "def",
    "class",
    "if",
    "for",
    "while",
    "with",
    "return",
    "import",
    "from"
])

rust_filters = file_type_filter(language=".rs", keywords=[
    "mod",
    "use",
    "let",
    "if",
    "else",
    "static",
    "const",
    "fn",
    "pub fn",
    "struct",
    "pub struct",
    "pub",
    "impl",
    "return"
])

html_filters = file_type_filter(language=".html")
css_filters = file_type_filter(language=".css")
js_filters = file_type_filter(language=".js")
r_filters = file_type_filter(language=".r")

full_filter_list = [
    python_filters,
    rust_filters,
    html_filters,
    css_filters,
    js_filters,
    r_filters
]
out_filename = "summary_stats_outfile"

# Adds all values that end with .py
for direct, _, filenames in walk(path_to_files):
    # Values to ignore to keep count accurate
    # These are folders which include files that aren't
    # Written by me
    if "venv" in direct:
        continue
    if "site-packages" in direct:
        continue
    if "$RECYCLE.BIN" in direct:
        continue
    if "node_modules" in direct:
        continue
    if "docker" in direct:
        continue
    if "wasm-bindgen" in direct:
        continue
    if ".obsidian" in direct:
        continue
    if "Program-Files" in direct:
        continue
    if "__MACOSX" in direct:
        continue
    if "app_ui" in direct:
        continue
    if "typenum-0a3c" in direct:
        continue
    if "startbootstrap-creative-gh-pages" in direct:
        continue

    # Finds files to add
    for filename in filenames:
        if "shop.css" in filename:
            continue
        if "start_bootstrap.css" in filename:
            continue
        for filters in full_filter_list:
            if filename.endswith(filters.language):
                out_list.append([path.join(direct, filename), filters])

# Attempts to Add all the data to book_list & adds to sum_of_lines counter
for i, (file, filters) in enumerate(out_list):
    try:
        with open(file, "r") as f:
            file_content = f.read()

            # Adds 1 to the file count and
            # gets the amount of each keyword in each section of the text
            filters.add_file()
            [filters.get_filters(string) for string in file_content.split("\n")]

            # Counts the amount of lines
            sum_of_lines += len(file_content.split("\n"))

            # Adds to the 'book' (full string of every file)
            book_list.append([out_list[i], file_content, len(file_content.split("\n"))])
    except Exception as e:
        print(out_list[i][0], e)

# Prints Statistics
summary_stats = f"amnt of lines: {sum_of_lines}\n"
summary_stats += f"amnt of files: {len(book_list)}\n"

# Adds Filter Statistics
for filter_value in full_filter_list:
    if filter_value.file_count == 0:
        continue
    summary_stats += filter_value.get_summary().strip() + "\n"
# Prints Values
print(summary_stats)

# Adds File Locations
out_string = ""
for i, value in enumerate(book_list):
    out_string += f"[{i}]\t({value[2]} lines)\t{value[0][0]}\n"

# Joins Both sets together
out_string += summary_stats

# Writes to a file
with open(f"{out_filename}.md", "w") as f:
    f.write(out_string)
    f.close()

exit()
