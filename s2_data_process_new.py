
###
import re
from collections import Counter
import spacy
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import json
import os

import ast
import random
from data_process import clean_conversation
# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Initialize NLTK components
lemmatizer = WordNetLemmatizer()
english_words = set(words.words())


def load_custom_words(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return set(json.load(file))
    else:
        return set()
    
# Load custom valid words and update the English words set
custom_words_file = "predefined_data/custom_valid_words.json"
custom_valid_words = load_custom_words(custom_words_file)
english_words.update(custom_valid_words)


# Map NLTK POS tags to WordNet POS tags
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def is_valid_word(word, pos_tag, named_entities):
    wordnet_pos = get_wordnet_pos(pos_tag)
    lemma = lemmatizer.lemmatize(word.lower(), pos=wordnet_pos)
    # Check for suffixes and proper nouns
    if word.endswith(('er', 'est', 'ed', 'ing','s','bility','ness','ment','less')) or pos_tag == 'NNP':
        return True
    # Check if the word is a named entity
    if word in named_entities:
        return True
    # Check if the lemma is in the set of English words
    return lemma in english_words

def check_conversation(conversation):
    invalid_lemmas = []
    # Split conversation by either \n or \n\n
    sentences = re.split(r'\n\n|\n', conversation)
    for sentence in sentences:
        doc = nlp(sentence)
        tokens = word_tokenize(sentence)
        pos_tags = pos_tag(tokens)
        named_entities = {ent.text.lower() for ent in doc.ents}  # Normalize named entities to lowercase
        
        for (word, tag) in pos_tags:
            if word.isalpha() and not is_valid_word(word, tag, named_entities):
                lemma = lemmatizer.lemmatize(word.lower(), pos=get_wordnet_pos(tag))
                invalid_lemmas.append(lemma)
                
    if invalid_lemmas:
        # print(f"Invalid lemmas: {invalid_lemmas}")
        return False, invalid_lemmas
    return True, invalid_lemmas

def filter_conversations(conversations):
    valid_conversations = []
    invalid_lemmas_ls = []
    for conversation in conversations:
        if not conversation.startswith("C:"):
            continue
        clean_con = clean_conversation(conversation)
        if clean_con:
            is_valid, invalid_lemmas = check_conversation(clean_con)
        # print(is_valid, invalid_lemmas)
            if is_valid:
                valid_conversations.append(conversation)
            invalid_lemmas_ls.extend(invalid_lemmas)
    
    # Find lemmas that occur more than once
    invalid_lemmas_counter = Counter(invalid_lemmas_ls)
    possible_lemmas_ls = [lemma for lemma, count in invalid_lemmas_counter.items() if count > 1]
    
    return valid_conversations, possible_lemmas_ls

# def filter_conversations(conversations):
#     valid_conversations = []
#     invalid_lemmas_ls = []
#     for conversation in conversations:
#         is_valid, invalid_lemmas = check_conversation(conversation)
#         # print(is_valid, invalid_lemmas)
#         if is_valid:
#             valid_conversations.append(conversation)
#         invalid_lemmas_ls.extend(invalid_lemmas)
    
#     # Find lemmas that occur more than once
#     invalid_lemmas_counter = Counter(invalid_lemmas_ls)
#     possible_lemmas_ls = [lemma for lemma, count in invalid_lemmas_counter.items() if count > 1]
    
#     return valid_conversations, possible_lemmas_ls


# Function to load JSON data
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)



def split_conversations(filtered_conversations):
    split_dicts = {}

    for activity, cleaned_conversations in filtered_conversations.items():
        random.shuffle(cleaned_conversations)
        total_conversations = len(cleaned_conversations)
        train_size = int(total_conversations * 0.7)
        val_size = int(total_conversations * 0.15)
            

        train_conversations = cleaned_conversations[:train_size]
        val_conversations = cleaned_conversations[train_size:train_size + val_size]
        test_conversations = cleaned_conversations[train_size + val_size:]

        split_dicts[activity] = {
            "train": train_conversations,
            "val": val_conversations,
            "test": test_conversations
        }

    return split_dicts

def save_conversations(file_name, conversations):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(conversations, file, indent=4)
    print(f"Splitted conversations for '{file_name}' saved to JSON file successfully!")







def main():
    my_list_str = os.getenv('MY_LIST', '[]')
    function_ls = ast.literal_eval(my_list_str)

    input_dir = os.getenv('INPUT_DIR', 'response_data/raw_conversations')
    output_dir = os.getenv('OUTPUT_DIR', 'response_data/split_conversations')

    for func in function_ls:
        f_path = os.path.join(input_dir, f"{func}.json")
        data = load_json(f_path)

        # Organize conversations by activity
        conversations = {}
        for dic in data[func]:
            activity = dic["activity"]
            conversation = dic["conversation"]
            if activity not in conversations:
                conversations[activity] = []
            conversations[activity].append(conversation)

        # Filter conversations by activity and check for invalid tokens
        filtered_conversations = {}
        possible_lemmas_ls = []
        for activity, conversation in conversations.items():
            valid_conversations, possible_lemmas = filter_conversations(conversation)
            filtered_conversations[activity] = valid_conversations
            possible_lemmas_ls.extend(possible_lemmas)
            print(f"Activity: {activity}, Valid conversations: {len(valid_conversations)}")
        print()
        print(f"Possible lemmas not to be removed: {set(possible_lemmas_ls)}")
        print()

        split_dicts = split_conversations(filtered_conversations)
        # Prepare data for saving
        train_dict = {act: dicts["train"] for act, dicts in split_dicts.items()}
        val_dict = {act: dicts["val"] for act, dicts in split_dicts.items()}
        test_dict = {act: dicts["test"] for act, dicts in split_dicts.items()}

        # Save data
        output_dir_s = os.path.join(output_dir, func)
        os.makedirs(output_dir_s, exist_ok=True)

        save_conversations(os.path.join(output_dir_s, "train.json"), train_dict)
        save_conversations(os.path.join(output_dir_s, "val.json"), val_dict)
        save_conversations(os.path.join(output_dir_s, "test.json"), test_dict)

if __name__ == "__main__":
    main()