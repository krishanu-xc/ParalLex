'''
Implement a distributed text processing engine. 
It should be able to read a set of .txt files present in a directory which contains textual data 
and answer a fixed set of questions which the user selects. 
The engine should be able to to utilize processing power of multiple cores
'''
import os
import sys
import time
import re

from multiprocessing import Pool

from collections import Counter
from collections import defaultdict

# helper fuctions
'''
getting the file count, no need for multiprocessing
'''

def get_file_count(directory: str) -> (int, list[str]):
    # get the file list in one single call
    file_count = 0
    file_list = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_list.append(os.path.join(directory, filename))
            file_count += 1
    return file_count, file_list

def get_word_count(file: str) -> int:
    count = 0
    with open(file) as f:
        for line in f:
            # ignore all the punctuations, use regex
            count += len(re.findall(r'\w+', line))
    return count

def get_distinct_word_count(file: str) -> dict:
    # use a default dict to store the word count
    word_count_dict = defaultdict(int)
    with open(file) as f:
        for line in f:
            for word in re.findall(r'\w+', line):
                word_count_dict[word.lower()] += 1
    return word_count_dict


# driver program
def main():
    
    # cores = cpu_count()
    cores = 3 # 3 instances max of 'engines'

    # if no argumens are passed, print usage
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)
    # check if file exists
    if not os.path.exists(sys.argv[1]):
        print("Error: file %s not found, please check if it exists." % sys.argv[1])
        sys.exit(1)
    # get the input file name
    input_file = sys.argv[1]

    # first line has the directory that contains all text files
    with open(input_file) as f:
        directory = f.readline().strip()
        # second line has the number of questions
        types = list(map(int, f.readline().strip().split()))

    '''
    1. total file count
    2. total word count
    3. total distinct word count
    4. top 100 most frequent words
    following the most expensive questions - if 3 or above, need a shared memory to store the word count
    '''

    # get the total file count
    t1 = time.time()
    file_count, file_list = get_file_count(directory)
    t2 = time.time()
    # calculate time elapsed in milliseconds
    fetch_elapsed_time = (t2 - t1) * 1000

    if 3 in types or 4 in types:
        # prefetch in background
        pref_t1 = time.time()
        pool = Pool(processes=cores)
        # create a list to store the results
        results = []
        # iterate through the file list
        for file in file_list:
            results.append(pool.apply_async(get_distinct_word_count, args=(file,)))
        # close the pool
        pool.close()
        # wait for all processes to finish
        pool.join()
        # merge the distinct word count dictionaries
        global_distinct_count_dict = defaultdict(int)
        for result in results:
            ddict = result.get()
            for key in ddict.keys():
                global_distinct_count_dict[key] += ddict[key]

        pref_t2 = time.time()
        elapsed_pref = (pref_t2 - pref_t1) * 1000

    for q in types:
        if q == 1:
            print("%d %f" % (file_count, fetch_elapsed_time))
        
        if q == 2:
            # get the total word count
            # parallelize the process
            t1 = time.time()
            pool = Pool(processes=cores)
            # create a list to store the results
            results = []
            # iterate through the file list
            for file in file_list:
                results.append(pool.apply_async(get_word_count, args=(file,)))
            # close the pool
            pool.close()
            # wait for all processes to finish
            pool.join()
            # get the total word count
            total_word_count = 0
            for result in results:
                total_word_count += result.get()
            t2 = time.time()
            elapsed_time = (t2 - t1) * 1000
            print("%d %f" % (total_word_count, elapsed_time))

            
            # # calculate time if not parallelized
            # t1 = time.time()
            # total_word_count = 0
            # for file in file_list:
            #     total_word_count += get_word_count(file)
            # t2 = time.time()
            # elapsed_time = (t2 - t1) * 1000
            # print("%d %f" % (total_word_count, elapsed_time))
            

            
        if q == 3:
            # get the total distinct word count
            # parallelize the process
            t1 = time.time()
            # get the total distinct word count
            distinct_word_count = len(global_distinct_count_dict.keys())
            t2 = time.time()
            elapsed_time = (t2 - t1) * 1000
            print("%d %f" % (distinct_word_count, elapsed_time + elapsed_pref))

            
            # # calculate time if not parallelized
            # t1 = time.time()
            # distinct_count_dict = defaultdict(int)
            # for file in file_list:
            #     ddict = get_distinct_word_count(file)
            #     for key in ddict.keys():
            #         distinct_count_dict[key] += ddict[key]
            # # get the total distinct word count
            # distinct_word_count = len(distinct_count_dict.keys())
            # t2 = time.time()
            # elapsed_time = (t2 - t1) * 1000
            # print("%d %f" % (distinct_word_count, elapsed_time))
            
        
        if q == 4:
            # get the top 100 most frequent words
            # we already have the global default dict with all the word counts
            # sort the dictionary by value

            # or use a counter, slightly better performance
            t3 = time.time()
            c = Counter(global_distinct_count_dict)
            top_100 = c.most_common(100)
            t4 = time.time()
            elapsed_time = (t4 - t3) * 1000
            for word, count in top_100:
                print("%s %d" % (word, count), end=' ')
            print("%f" % (elapsed_time + elapsed_pref))

        if q not in [1, 2, 3, 4]:
            print("Error: question type %d not supported." % q)
            sys.exit(1)

if __name__ == "__main__":
    main()