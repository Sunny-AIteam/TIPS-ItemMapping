import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

def test():
    print('workong!')
    return 

def sort_item_name(df):

    # Drop duplicates based on all columns
    new_df = df.drop('price', axis=1)
    new_df = new_df.drop_duplicates()

    # Calculate text length and sort by 'text_length'
    new_df['text_length'] = new_df['productTitle'].apply(len)
    sorted_df = new_df.sort_values(by='text_length')

    # Drop the temporary 'text_length' column if not needed
    sorted_df = sorted_df.drop(columns='text_length')

    return sorted_df


def select_brand(df, brand_name):
    # Filter DataFrame for the given brand
    new_df = df[df['brand'] == brand_name]

    # Drop duplicates based on all columns
    new_df = new_df.drop('price', axis=1)
    new_df = new_df.drop_duplicates()

    # Calculate text length and sort by 'text_length'
    new_df['text_length'] = new_df['productTitle'].apply(len)
    sorted_df = new_df.sort_values(by='text_length')

    # Drop the temporary 'text_length' column if not needed
    sorted_df = sorted_df.drop(columns='text_length')

    return sorted_df


def filter_brands(nested_list, target_word):
    filtered_list = []

    for inner_list in nested_list:
        filtered_inner_list = [word for word in inner_list if word != target_word]
        filtered_list.append(filtered_inner_list)

    return filtered_list


def filter_words(nested_list, target_words):
    filtered_list = []

    for inner_list in nested_list:
        filtered_inner_list = inner_list.copy()  # Create a copy to avoid modifying the original list
        for target_word in target_words:
            if target_word != '':
                filtered_inner_list = [word for word in filtered_inner_list if str(target_word) not in str(word)]
        filtered_list.append(filtered_inner_list)

    return filtered_list


def flatten_once(nested_list):
    return [item for sublist in nested_list for item in (sublist if isinstance(sublist, list) else [sublist])]



def plot_word_histogram(nested_list):
    # Flatten the nested list
    flat_list = [word for sublist in nested_list for word in sublist]

    # Count the frequency of each word
    word_counts = Counter(flat_list)

    # Sort words and frequencies in descending order
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    print(sorted_word_counts)
    words, frequencies = zip(*sorted_word_counts)

    # Plot the word histogram
    plt.figure(figsize=(6, 4))
    plt.bar(words, frequencies, color='blue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Word Histogram')
    plt.xticks(rotation=45, ha='right')
    plt.show()

    return sorted_word_counts


def split_text_to_words(row):
    """
    Helper function to be used with apply. Splits the text in a row into words.

    Parameters:
    - row (pd.Series): A row in the DataFrame.

    Returns:
    - list: A list of words from the text in the row.
    """
    text = str(row)
    words = text.split()
    return words


def split_text_column_to_words(dataframe, column_name):
    """
    Takes a DataFrame and a column containing text, splits the text into words using the apply function, 
    and returns a list of words for each row in the specified column.

    Parameters:
    - dataframe (pd.DataFrame): The DataFrame containing the text column.
    - column_name (str): The name of the column containing text.

    Returns:
    - list of lists: A list of lists where each sublist contains words from the corresponding row.
    """
    if column_name not in dataframe.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    words_list = dataframe[column_name].apply(split_text_to_words).tolist()

    return words_list

