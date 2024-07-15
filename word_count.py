import re
import pandas as pd
import sys
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

# read lines in plain text file
def get_word_counts(file_path, word_count_dict):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # replace all non-alphabet characters by spaces
            updated_line = re.sub('[^a-zA-Z]', ' ', line)
            # get all words in the line by splitting on spaces
            words = updated_line.split(' ') 

            for word in words:
                word_lower = word.lower()
                # increment count of word if present in pre-defined list
                if word_lower in word_count_dict:
                    word_count_dict[word_lower][0] += 1


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: python word_count.py <predefined words path> <sample file path>')
        sys.exit(1)
    
    start_time = time.time()

    words_file_path = sys.argv[1]
    sample_file_path = sys.argv[2]
    word_count_dict = get_predefined_words(words_file_path)
    get_word_counts(sample_file_path, word_count_dict)

    # extract pre-defined words with non-zero count in the file
    words_found_dict = {v[1]: v[0] for k, v in word_count_dict.items() if v[0] != 0}

    # display the result
    df = pd.DataFrame(list(words_found_dict.items()), columns=['Predefined word', 'Match count'])
    print(df.to_string(index=False))

    # display total execution time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {elapsed_time} seconds')