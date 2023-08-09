# ParalLex

A naïve implementation of a distributed text processing engine, made in partial fulfillment of the hiring challenge for [**E6Data**](https://www.e6data.com/).

## Table of Contents

- [ParalLex](#parallex)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
  - [Usage](#usage)
    - [Input file format](#input-file-format)
  - [Project Architecture](#project-architecture)
  - [Layout](#layout)
  - [Performance](#performance)

## Getting Started

1. Environment Setup
    - Ensure you have Python 3.x installed on your system. You can download it from the official Python website [here](https://www.python.org/downloads/).
    - Check that Python is properly installed by running `python --version` or `python3 --version` (on some machines) in your terminal.
  
2. Dependencies
   - All the dependencies are installed by default with Python 3.x. You can check the version of the dependencies by running `pip freeze` in your terminal. A `requirements.txt` file is not provided as it is not required.

## Usage

The program can be run by executing the following command in your terminal:

```zsh
python main.py <input_file>
```

### Input file format

The input file should be a text file with the following format:

- Line 1: The path to a directory containing the input files.
- Line 2: A list of space seperated integers, each denoting a specific operation to be performed on the input files.
  - 1 - Count the total number of files in the directory.
  - 2 - Count the total number of words across all files in the directory.
  - 3 - Count the total number of *distinct* words across all files in the directory.
  - 4 - List the top 100 words with frequencies in descending order of frequency of occurence.

An example of the input file is given below:

```text
/Users/User1/Desktop/texts
1 2 3 4
```

## Project Architecture

A class based implementation was avoided in order to keep the code modular and easy to understand.
A class based imlementation also leads to several complications when it comes to multiprocessing, solving which are beyond the scope of this project and an unnecessary overhead.

The project is divided into a main module and several helper modules. The main module is responsible for parsing the input file and calling the appropriate functions from the helper modules. The helper modules are responsible for performing the actual operations on the input files.

The helper modules are as follows:

- `get_file_count(dir: str) -> (int, list[str]):`: Returns the total number of files and the paths to each text file in the directory.
- `get_word_count(file_path: str) -> int:`: Returns the total number of words in the file. uses the `re.findall()` module to match words using RegEx, which increases code readability and gives a slight performance boost over the `split()` method, which would require extra steps to ignore punctuation.
- `get_distinct_word_count(file_path: str) -> dict:`: Returns the total number of distinct words in the file. `word.lower()` is used to ensure that words are counted appropriately due to case sensitivity.
- The top 100 words with frequencies in descending order of frequency of occurence are obtained by using the `Counter()` module from the `collections` library. The `most_common()` method is used to obtain the top 100 words with their frequencies.

The multiprocessing module is used to parallelize the operations on the input files. The `Pool()` class is used to create a pool of processes, which are then used to perform the operations on the input files.
The `apply_async()` method is used over `map()` as the order of return values doesn't concern us.

## Layout

```text
function implementations
...
...
main() module
```

## Performance

Here we compare the performance of the program with and without multiprocessing.

The following table shows the time taken to perform the operations on a directory containing 4000 text files, with around 1.7 Million words in total. Results are averaged over 5 runs.

| Operation | Time taken without multiprocessing (ms) | Time taken with multiprocessing (ms) |
| :-------: | :------------------------------------: | :----------------------------------: |
| Getting the total number of words | 606.455 | 399.110 |
| Getting the total number of distinct words | 1514.011 | 731.016 |

the results are obtained by running the program on a 2020 MacBook Pro with a 2.4 GHz 8-Core Intel Core i5 processor and 16 GB of RAM.
