import random
import os
import json
import re


def contains_numbers(token):
    """Check if the token contains any numbers in invalid format."""
    if any(char.isdigit() for char in token):
        # Keep the token if it matches time or specific allowed patterns
        if re.match(r'^(\d+(\.\d+)?)([:,.-]?)$', token):
            return False
        if re.match(r'^\d+:\d+$', token):  # Keep time tokens like "7:00"
            return False
        if re.match(r'^\d+-minute$', token):  # Keep tokens like "20-minute"
            return False
        return True
    return False

# def delete_last_question(conversation):
#     """Delete the question if it's the last sentence in the conversation."""
#     if re.search(r'\nC:.*$', conversation):
#         p = r'\nC:.*$'
#         conversation = re.sub(p, '', conversation)
#     return conversation
def delete_last_question(conversation):
    """Delete the question if it's the last sentence in the conversation."""
    # Check for the pattern \n\nC: or \nC: at the end of the conversation
    if re.search(r'(\n\nC:|\nC:).*$', conversation):
        # Pattern to match \n\nC: or \nC: at the end
        pattern = r'(\n\nC:|\nC:).*?$'
        conversation = re.sub(pattern, '', conversation)
    return conversation




# def clean_conversation(conversation):
#     """
#     Clean a single conversation based on specified rules:
#     1. Remove conversations that contain tokens with numbers
#     2. Remove sequences of more than two continuous hyphens
#     3. Replace double newlines (\n\n) with a single newline (\n)
#     4. Remove < and > tags along with their contents.
#     5. Remove words that are more than 18 characters long.
#     """

#     # Delete the last sentence
#     # print(conversation)
#     conversation = delete_last_question(conversation)

#     # Split the conversation into words
#     tokens = conversation.split()
    

#     # Check for tokens with numbers and delete the conversation if any are found
#     for token in tokens:
#         if contains_numbers(token):
  
#             print(f"Offending token: {token}")
#             return None
#         if len(token) > 18:
#             print(f"Offending token: {token}")
#             return None


#     # Join the tokens back into a string
#     valid_text = ' '.join(tokens)

#     # Remove sequences of more than two continuous hyphens
#     valid_text = re.sub(r'-{3,}', '', valid_text)

#     # Replace double newlines with a single newline
#     valid_text = re.sub(r'\n\n+', '\n', valid_text)

#     # Remove <> tags and the content inside them
#     valid_text = re.sub(r'<[^>]*>', '', valid_text)

#     return valid_text.strip()


# Define the pattern for filtering out conversations
filter_pattern = re.compile(r'\*.*?\*')

def clean_conversation(conversation):
    """
    Clean and filter a single conversation based on specified rules:
    1. Filter out conversations containing specific patterns (e.g., *words*).
    2. Remove conversations that contain tokens with numbers.
    3. Remove sequences of more than two continuous hyphens.
    4. Replace double newlines (\n\n) with a single newline (\n).
    5. Remove < and > tags along with their contents.
    6. Remove words that are more than 18 characters long.
    """

    # Check if the conversation matches the filter pattern
    if filter_pattern.search(conversation):
        # print(f"Filtered out conversation: {conversation}")
        return None

    # Delete the last sentence
    conversation = delete_last_question(conversation)

    # Split the conversation into words
    tokens = conversation.split()

    # Check for tokens with numbers and delete the conversation if any are found
    for token in tokens:
        if contains_numbers(token):
            print(f"Offending token: {token}")
            return None
        if len(token) > 18:
            print(f"Offending token: {token}")
            return None

    # Join the tokens back into a string
    valid_text = ' '.join(tokens)

    # Remove sequences of more than two continuous hyphens
    valid_text = re.sub(r'-{3,}', '', valid_text)

    # Replace double newlines with a single newline
    valid_text = re.sub(r'\n\n+', '\n', valid_text)

    # Remove <> tags and the content inside them
    valid_text = re.sub(r'<[^>]*>', '', valid_text)

    return valid_text.strip()