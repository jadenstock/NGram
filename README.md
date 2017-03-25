# NGram

## Using the data structure.
In NGram.py there is an NGram class. This will hold an NGram language model. After you create an instance of this class you can train it on your data by using NGram.train_from_file(file_name). The method will treat each line in the file as a new sentence. You can then get the log probability of seeing a given sentence using the log_probability_of_sentence method. You can test how good the language model is by computing the perplexity score of another file using the perplexity method.
