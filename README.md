# Illumio Technical Assessment
# Word Count Generator

## Author
**Name:** Sahil Nagpal  
**Email:** sahil.nagpal@outlook.in

## Execution Commands

### Serial Execution:
```bash
python word_count.py <predefined words file path> <sample text file path>
```

### Parallel Execution:
```bash
python word_count_parallel.py <predefined words path> <sample file path> <number of processes>
```

## Testing Process
1. Used the 10000 words list provided by Google for the predefined words (words.txt) ([Google 10000 English Words List](https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt)). 
2. Used the Kaggle random sentences dataset for the sample text (sample.txt). Repeated the 724 sentences to create a file size of 20MB.
([Kaggle Random Sentences Dataset](https://www.kaggle.com/datasets/nikitricky/random-english-sentences))
3. Executed the Python code (both serial and parallel) on these files to get the word count.
4. Compared the resulting word count with "Find" results in Sublime Text.
5. Compared the results between the different execution methods by exporting them to text files and comparing the outputs.
6. Benchmarked the performance of the code by calculating the execution time using the `time` module.

## Performance
Serial execution performs better due to the small size of inputs. The cost of dictionary aggregation and thread overhead causes the parallel method to perform poorly. However, with larger inputs, parallel execution is expected to perform better.

## Assumptions
- The predefined words are proper English words containing only alphabets.
- Each line in the predefined words file contains only one word.
- The Pandas library is installed in Python (used for displaying the final word count).
- The final result prints the words in the same casing as the predefined words file.
- The sample text file does not contain contractions (e.g., "it's" for "it is").

## Possible Improvements
- Use MapReduce for larger files.
- Include contractions by modifying the regular expression to handle single quotes.
