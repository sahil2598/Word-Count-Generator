import re
import pandas as pd
import sys
import multiprocessing
import time

# get all pre-defined words
def get_predefined_words(file_path):
    word_count_dict = dict()
    with open(file_path, 'r') as predefined_words_file:
        words_lines = predefined_words_file.readlines()

        # initialize pre-defined words in dictionary with zero count
        for word_line in words_lines:
            word = word_line.strip()
            # stores the original casing of pre-defined word
            word_count_dict[word.lower()] = [0, word]
    
    return word_count_dict

def process_chunk(lines, shared_dict, word_count_dict):
    # local dictionary for the process to avoid unnecessary atomic updates to shared dictionary
    local_dict = dict()
    for line in lines:
        # replace all non-alphabet characters by spaces
        updated_line = re.sub('[^a-zA-Z]', ' ', line)
        # get all words in the line by splitting on spaces
        words = updated_line.split(' ') 

        for word in words:
            word_lower = word.lower()
            # increment count of word if present in pre-defined list
            if word_lower in word_count_dict:
                if word_lower not in local_dict:
                    local_dict[word_lower] = word_count_dict[word_lower]
                local_dict[word_lower][0] += 1
    
    # add word counts in local dictionary to shared dictionary
    for k, v in local_dict.items():
        new_val = [shared_dict[k][0] + v[0], v[1]]
        shared_dict[k] = new_val


# read lines in plain text file
def get_word_counts(file_path, word_count_dict, num_procs):
    # use multiprocessing manager to maintain shared dictionary between processes
    manager = multiprocessing.Manager()
    shared_dict = manager.dict(word_count_dict)

    with open(file_path, 'r') as file:
        lines = file.readlines()
        # divide lines in the file into chunks
        chunk_size = len(lines) // num_threads
        chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
        process_list = []
        for i in range(num_threads):
            # assign chunks to processes to execute in parallel
            process_list.append(multiprocessing.Process(target=process_chunk, args=(chunks[i], shared_dict, word_count_dict)))
            process_list[i].start()

        for i in range(num_threads):
            process_list[i].join()
    
    return shared_dict


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('Usage: python word_count_parallel.py <predefined words path> <sample file path> <number of processes>')
        sys.exit(1)

    start_time = time.time()
    
    words_file_path = sys.argv[1]
    sample_file_path = sys.argv[2]
    num_procs = int(sys.argv[3])
    word_count_dict = get_predefined_words(words_file_path)
    shared_dict = get_word_counts(sample_file_path, word_count_dict, num_procs)

    # extract pre-defined words with non-zero count in the file
    words_found_dict = {v[1]: v[0] for k, v in shared_dict.items() if v[0] != 0}

    # display the result
    df = pd.DataFrame(list(words_found_dict.items()), columns=['Predefined word', 'Match count'])
    print(df.to_string(index=False))

    # display total execution time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {elapsed_time} seconds')