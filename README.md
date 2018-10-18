# Article Search System 
> A Search Engine written in Python3.

Below is the list of implemented functionalities in this rank retrival model. These can be multi-purposely used to search for queries from the corpus in `English` and `Arabic` languages.

## Functionality Implemented

  1. Searching top 10 articles based on a given query.
  2. Comparing cosine-similarity between 2 articles present in the corpus.
  3. Implementation of Wilcard Queries.
  4. Term Auto-completion for search suggestions using tries.


# The Corpus 
 * [English Corpus](https://dumps.wikimedia.org/enwiki/latest/) - from where English-articles were downloaded and processed.
 * [Arabic Corpus](https://dumps.wikimedia.org/arwiki/latest/) - from where Arabic-articles were downloaded and processed.


## Software frameworks used:

 * [python-nltk](http://www.nltk.org/) - NLTK is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces
 
    * Install NLTK:
    
    ```$ sudo pip install -U nltk```
   
   
   * Install Numpy: 
    
    ```$ sudo pip install -U numpy```
   
   
   * Test installation:
    
    ```
   $ python3 
   >>> import nltk
   ```

 * [python-flask](https://www.loomio.org/) - frame work to creade a frontend interactive application in python. [Installing flask in python](http://hanzratech.in/2015/01/16/setting-up-flask-in-ubuntu-14-04-in-virtual-environment.html)
 
 * [WikiExtractor](https://github.com/attardi/wikiextractor) Python script that extracts and cleans text from enwiki dumps.
 
 * [arwiki_parser](https://github.com/owo/arwiki_parser) Python script that extracts and cleans text from arwiki dumps.

 
## Platforms:

 * This can be used on any browser that support javascript, css and jquery provided we have the server set up.
 * To set up server we need python with both python nltk and flask installed.
 
## Project Extention
 * Creating Query Logs and using machine learning technique to use logs to implement more efficient query searching in corpus.
