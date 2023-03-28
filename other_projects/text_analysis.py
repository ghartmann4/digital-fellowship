"""
Reads 110 books contained in an existing folder, and computes word counts and unique word counts for each. This data is stored in a pandas DataFrame along with the book’s language, author, and title.
A loglog plot of the number of unique words as a function of book length is created, and color coded by language.
"""

import os
import pandas as pd

def read_book(title_path):
    """
    read book and return it as a string
    """

    with open(title_path, "r", encoding ="utf8") as current_file:
        text = current_file.read()
        text = text.replace("\n", "").replace("\r", "")
    return text


def count_words(text):
    """
    Count number of times each word occurs in text (str)
    Return dictionary word_count where keys are unique words
    and values are word counts
    """
    
    word_counts = {}
    for word in text.split(" "):
        # known word
        if word in word_counts:
            word_counts[word] += 1
        # new word
        else: 
            word_counts[word] = 1
        
    return word_counts

def word_stats(word_counts):
    """Return number of unique words and word frequencies"""
    num_unique = len(word_counts) #number of unique words
    counts = word_counts.values()
    return (num_unique, counts)

"""
This folder contains about one hundred books organized into folders by language, author, and title
The text files are available for free from Project Gutenberg
"""

book_dir = "E:/My Documents/Documents/Python Harvard Course Book Files"


stats = pd.DataFrame(columns = ("language", "author", "title", "length", "unique"))
title_num = 1

"""
loop over each book in the folder and store the stats in a pandas DataFrame
"""
for language in os.listdir(book_dir):
    for author in os.listdir(book_dir + "/" + language):
        for title in os.listdir(book_dir + "/" + language + "/" + author):
            inputfile = book_dir + "/" + language + "/" + author + "/" + title
            print(inputfile)
            text = read_book(inputfile)
            (num_unique, counts) = word_stats(count_words(text))
            stats.loc[title_num] = language, author.capitalize(), title.replace(".txt", ""), sum(counts), num_unique
            title_num += 1
            
# test to make sure this works:          
print(stats.head())

# now that the data is stored, make plots of it:

import matplotlib.pyplot as plt

plt.figure(figsize = (10,10))
subset = stats[stats.language == "English"]
plt.loglog(subset.length, subset.unique, "o", label = "English", color = "crimson")

subset = stats[stats.language == "French"]
plt.loglog(subset.length, subset.unique, "o", label = "French", color = "forestgreen")

subset = stats[stats.language == "German"]
plt.loglog(subset.length, subset.unique, "o", label = "German", color = "orange")

subset = stats[stats.language == "Portuguese"]
plt.loglog(subset.length, subset.unique, "o", label = "Portuguese", color = "blueviolet")

plt.legend()
plt.xlabel("Book Length")
plt.ylabel("Number of unique words")

plt.savefig("Language_Plot.pdf")
