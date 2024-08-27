# download necessary package
import subprocess
import sys

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}: {e}")
    else:
        print(f"{package} installed successfully")

def main():
    required_packages = ["rouge-score", "bert-score", "nltk"]

    for package in required_packages:
        try:
            __import__(package)
            print(f"{package} is already installed")
        except ImportError:
            print(f"{package} is not installed. Installing now...")
            install_package(package)

    # Download necessary NLTK data
    try:
        import nltk
        nltk.download('punkt')
        print("NLTK data 'punkt' downloaded successfully")
    except Exception as e:
        print(f"Failed to download NLTK data 'punkt': {e}")

if __name__ == "__main__":
    main()

import nltk
from nltk import word_tokenize
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate import meteor

from rouge_score import rouge_scorer
from transformers import BartTokenizer, BartForConditionalGeneration, BartModel
from bert_score import score

# import evaluate

import torch
import json
import random
import numpy as np
import re


def calculate_bleu(reference_texts, hypothesis_text, ngram_order=4, smoothing=True, highest_score=True):
    """
    Calculate BLEU scores for a single hypothesis text against multiple reference texts.
    
    Parameters:
    - reference_texts: List of reference texts (either a list of strings or a list of lists of strings).
    - hypothesis_text: Single hypothesis text (string).
    - ngram_order: Maximum n-gram order to use for BLEU calculation.
    - smoothing: Whether to apply smoothing.
    - highest_score: True to calculate the highest score, False to calculate the average score.
    
    Returns:
    - bleu_scores: List of BLEU scores (highest or average) for each set of reference texts.
    """
    smooth_fn = SmoothingFunction().method1 if smoothing else None
    weights = tuple((1.0 / ngram_order) for _ in range(ngram_order))
    
    hypothesis_tokens = hypothesis_text.split()


    scores = []
    for ref in reference_texts:
        ref_tokens = ref.split()
        score = sentence_bleu([ref_tokens], hypothesis_tokens, weights=weights, smoothing_function=smooth_fn)
        scores.append(score)
        
    if highest_score:
        highest_bleu_score = max(scores)
        bleu_scores=round(highest_bleu_score, 4)
    else:
        average_bleu_score = sum(scores) / len(scores)
        bleu_scores=round(average_bleu_score, 4)
    
    return bleu_scores


def cal_rouge_score(reference_list, candidate, ngram_order=['rouge1', 'rouge2', 'rougeL'], highest_score=True):
    """
    Calculate ROUGE score (f-measure) of candidate (highest or average) against each reference in the reference list.
   
    
    Parameters:
    - reference_list: List of reference texts.
    - candidate: Candidate text to compare against reference texts.
    - ngram_order: List of n-grams to use for ROUGE calculation.
    - highest_score: True to calculate the highest score, False to calculate the average score.
    
    Returns:
    - score_dict: Dictionary containing ROUGE scores for each n-gram order.
    """
    
    # Initialize the ROUGE scorer
    scorer = rouge_scorer.RougeScorer(ngram_order, use_stemmer=True)


    # Initialize score dicts
    score_dicts = {ngram:[] for ngram in ngram_order}

    # Calculate ROUGE 
    for ref in reference_list:
        scores = scorer.score(ref, candidate)

        for n_gram in ngram_order:
            score_dicts[n_gram].append(scores[n_gram].fmeasure)
            
        
    # final score depending on highest/mean
    final_dict = {}

    for n_gram, score in score_dicts.items():
        
        if highest_score:
            final_dict[n_gram] = round(np.max(score), 4)
        else:
            final_dict[n_gram] = round(np.mean(score), 4)


    return final_dict

def cal_meteor(ref_ls, cad, highest_score=True):
    """
    calculate meteor score

    Para:
    - ref_ls: reference list of utterances
    - cad: candidate/prediction string
    - highest_score: True to calculate the highest score, False to calculate the average score.

    Return:
    highest or average score
    """

    scores=[]
    for ref in ref_ls:
        score = round(meteor([word_tokenize(ref)], word_tokenize(cad)), 4)
        scores.append(score)
        # print(score)

    if highest_score:
        final_score=np.max(scores)
    else:
        final_score=np.mean(scores)

    return final_score

def cal_bert(reference_sentences, candidate_sentence, lang="en", highest_score=True):
    """
    Calculate BERTScore for a single candidate sentence against multiple reference sentences.
    
    Parameters:
    - reference_sentences: List of reference sentences.
    - candidate_sentence: Single candidate sentence.
    - lang: Language of the sentences.
    - highest_score: True to return the highest score, False to return the average score.
    
    Returns:
    - bert_scores: Dictionary containing BERTScore Precision, Recall, and F1 (highest or average).
    """
    # Create a list of the candidate sentence repeated for each reference sentence
    candidate_sentences = [candidate_sentence] * len(reference_sentences)
    
    # Calculate BERTScore
    P, R, F1 = score(candidate_sentences, reference_sentences, lang=lang, verbose=True)
    
    if highest_score:
        # Calculate and return the highest BERTScore metrics
        bert_scores = {
            "Precision": round(P.max().item(), 4),
            "Recall": round(R.max().item(), 4),
            "F1": round(F1.max().item(), 4)
        }
    else:
        # Calculate and return the mean BERTScore metrics
        bert_scores = {
            "Precision": round(P.mean().item(), 4),
            "Recall": round(R.mean().item(), 4),
            "F1": round(F1.mean().item(), 4)
        }
    
    return bert_scores


# def clean_str(string):
#     """
#     extract only the questions in a list
    
#     return:
#     a list of each question string[Q1, Q2,...] in a FQ set
#     """
    


#     # Regular expression to find sentences starting with 'C:'
#     pattern = r'(?:\n*\n*C: (.*?))(?=\n*\n*P:|$)'

#     # Find all matches
#     matches = re.findall(pattern, string, re.DOTALL)

#     # Strip leading/trailing whitespace and remove newline characters
#     cleaned_matches = [match.strip().replace('\n', ' ') for match in matches]

#     # Print the result
#     return cleaned_matches

def clean_str(string):
    """
    Extracts questions from the given string and returns them as a list.
    Each question starts with 'C:' and ends before 'P:' or the end of the string.
    
    Parameters:
    string (str): The input string containing the questions.
    
    Returns:
    List[str]: A list of questions with leading/trailing whitespace removed.
    """
    
    # Regular expression to find sentences starting with 'C:' or 'C: ' and ending before 'P:' or end of string
    pattern = r'(?:\n*\n*C:\s*(.*?))(?=\n*\n*P:\s*|$)'
    
    # Find all matches
    matches = re.findall(pattern, string, re.DOTALL)
    
    # Strip leading/trailing whitespace and replace newline characters with a space
    cleaned_matches = [match.strip().replace('\n', ' ') for match in matches]
    
    return cleaned_matches


def count_empty_ls(function, ty, empty_fqs_few):
    """
    count possible empty lists where there are no fq for one conversation
    """
    
    empty_ls =[act for act, n in empty_fqs_few[function][ty]]
    # print(empty_ls)

    from collections import Counter

    # Create a Counter object
    empty_counts = Counter(empty_ls)

    
    # Print the counts of each element
    return empty_counts

def check_fq_conv_num(act, conv, empty_counts, lenth):
    """
    check if the extracted fq lists num match and conversation num 
    """
    empty_num = 0
    if act in empty_counts.keys():
        empty_num = empty_counts[act]
    conv_num = len(list(conv.keys()))-empty_num

    if not lenth==conv_num:
        print(f"fq and conversation num of {act} NOT match")
        return False
    return True

def extract_question_noind(function, ty, candi_path, empty_fqs):
    """
    return list of fqs of each conversation of each activity
    """
    with open(candi_path, 'r') as file:
        candi_func = json.load(file)

    all_cad1 = {}
    
    empty_counts = count_empty_ls(function, ty, empty_fqs)
    for activity, conversations in candi_func.items():  
        if activity not in all_cad1:
            all_cad1[activity] = []

        for conversation_ind, fqs_list in conversations.items():  

    #         check if fqs_list empty
            if (activity, conversation_ind) in empty_fqs[function][ty]:
                continue
#             extract one fq for each conversation
            for fq in fqs_list:
                cleaned_list = clean_str(fq)

                if cleaned_list:  # Check if the cleaned list empty
                    all_cad1[activity].append(cleaned_list) #only one fq for each conversation 
                    break
                    
#         check if the extracted fq lists num match and conversation num (one con, one fq)
        if not check_fq_conv_num(activity, conversations, empty_counts, len(all_cad1[activity])):
            break
    
    return all_cad1

def extract_ref_utter(ref_4conver):
    """
    Extract reference lists. Each list contains multiple references against one utterance.

    Return:
    A list of lists, where each inner list corresponds to a specific utterance's references.

    Para:
    ref_4conver: A list of lists, each containing continuous utterances.
    """

    # Determine the maximum number of utterances
    max_utterances = max(len(sublist) for sublist in ref_4conver)

    # Initialize a list of lists to store references for each utterance
    utterances = [[] for _ in range(max_utterances)]

    # Iterate over the sublists and extract sentences by their positions
    for sublist in ref_4conver:
        for i in range(len(sublist)):
            utterances[i].append(sublist[i])

    return utterances

def extract_ref_lss (function, ty, ref_path, empty_fqs):
    """
    extract reference lists containing multiple references against one utterance
    """

    with open(ref_path, 'r') as file:
        candi_func = json.load(file)

    all_cad1 = {}

    empty_counts = count_empty_ls(function, ty, empty_fqs)
    for activity, conversations in candi_func.items():  
        if activity not in all_cad1:
            all_cad1[activity] = []

        for conversation_ind, fqs_list in conversations.items():  

    #         check if fqs_list empty
            if (activity, conversation_ind) in empty_fqs[function][ty]:
                continue
    #         extract multiple fqs for each conversation 
            fqs_4conver=[]

            for fq in fqs_list:
                cleaned_list = clean_str(fq)

                if cleaned_list:  # Check if the cleaned list is not empty

                    fqs_4conver.append(cleaned_list) # fqs for each conversation 

    #       extract multiple refs for each utterance (only three references and maxium three utterances will be compared)
            refer_ls = extract_ref_utter (fqs_4conver)
            # print(refer_ls)
            # print()
            all_cad1[activity].append(refer_ls)

    #         check ref_list num and conver num
        # for act, conv in candi_func.items():
        if not check_fq_conv_num(activity, conversations, empty_counts, len(all_cad1[activity])):
            break



    return all_cad1





def evaluate_conversations_new(cad_ls, ref_lss, cal_high=True):
    """
    evaluate_conversations scores of bleu, rouge, meteor
    """
    
    scores_all = {str(i): [] for i in range(len(cad_ls))}
    
    for n, cad_l in enumerate(cad_ls):
        cad_l_bleu = []
        cad_l_rouge = []
        cad_l_meteor = []
        cad_l_bert = []
        
        # print(cad_l, ref_lss[n])
        
        min_length = min(len(cad_l), len(ref_lss[n]))
        cad_l = cad_l[:min_length]
        ref_lss[n] = ref_lss[n][:min_length]
        
        # print()
        # print(cad_l, ref_lss[n])

        for cad, ref_l in zip(cad_l, ref_lss[n]):
            # print(cad, ref_l)
            
            
#             check if there is enough reference nymber for utterance

#             min_length = min(len(cad), len(ref_l))
#             cad = cad[:min_length]
#             ref_l = ref_l[:min_length]
            
#             print()
#             print(cad, ref_l)
#             print()
            ngram_bleu = 4
            cad_l_bleu.append(calculate_bleu(ref_l, cad, ngram_order=ngram_bleu, smoothing=True, highest_score=cal_high))
            cad_l_rouge.append(cal_rouge_score(ref_l, cad, highest_score=cal_high))
            cad_l_meteor.append(cal_meteor(ref_l, cad, highest_score=cal_high))
            cad_l_bert.append(cal_bert(ref_l, cad, lang="en", highest_score=cal_high))# append one dictionary of each cad with keys: Precision, Recall, F1
        # print(cad_l_bert)
#             print(cad_l_bleu)
                

        
        cad_l_rouges = {}
        for dict_scores in cad_l_rouge:
            for k, v in dict_scores.items():
                if k not in cad_l_rouges:
                    cad_l_rouges[k] = [v]
                else:
                    cad_l_rouges[k].append(v)

        scores_all[str(n)] = [
            {f"bleu{ngram_bleu}": round(np.mean(cad_l_bleu),4)},
            {"rouge": {k: round(np.mean(v),4) for k, v in cad_l_rouges.items()}},
            {"meteor": round(np.mean(cad_l_meteor),4)},
            {"bert": {key: round(np.mean([i[key] for i in cad_l_bert]), 4) for key in ["Precision", "Recall", "F1"]}}
        ]

    return scores_all


def ave_type_cate(metrics):
    """
    average_scores of each fq_type of each category

    Para:::
    metrics: dict of all scores of each fq_type of each category
    """
    # results = {}
    # for key in metrics.keys(): #key is '0' or '1'
    total_bleu4 = []
    total_rouge1 = []
    total_rouge2 = []
    total_rougeL = []
    total_meteor = []
    total_precision = []
    total_recall = []
    total_f1 = []
        # Iterate over each entry in '0' and '1'      
    for sub_key in metrics.keys(): 
        values = metrics[sub_key]
        for value in values:
            if 'bleu4' in value:
                total_bleu4.append(value['bleu4'])
            if 'rouge' in value:
                total_rouge1.append(value['rouge']['rouge1'])
                total_rouge2.append(value['rouge']['rouge2'])
                total_rougeL.append(value['rouge']['rougeL'])
            if 'meteor' in value:
                total_meteor.append(value['meteor'])
            if 'bert' in value:
                total_precision.append(value['bert']['Precision'])
                total_recall.append(value['bert']['Recall'])
                total_f1.append(value['bert']['F1'])

        # Calculate averages
    results = {
            'bleu4': round(np.mean(total_bleu4), 4),
            'rouge1': round(np.mean(total_rouge1), 4),
            'rouge2': round(np.mean(total_rouge2), 4),
            'rougeL': round(np.mean(total_rougeL), 4),
            'meteor': round(np.mean(total_meteor), 4),
            'bert': {
                'Precision': round(np.mean(total_precision), 4),
                'Recall': round(np.mean(total_recall), 4),
                'F1': round(np.mean(total_f1), 4)
            }
        }
    
    return results


import numpy as np
import math

def ave_type_cate_exc(metrics):
    """
    average_scores of each fq_type of each category with exception where there is no key or value or nan in the dataset

    Para:::
    metrics: dict of all scores of each fq_type of each category
    """
    total_bleu4 = []
    total_rouge1 = []
    total_rouge2 = []
    total_rougeL = []
    total_meteor = []
    total_precision = []
    total_recall = []
    total_f1 = []

    for sub_key in metrics.keys():
        values = metrics[sub_key]
        for value in values:
            try:
                if 'bleu4' in value and not math.isnan(value['bleu4']):
                    total_bleu4.append(value['bleu4'])
            except (KeyError, TypeError, ValueError) as e:
                print(f"Error processing 'bleu4' in {sub_key}: {e}")

            try:
                if 'rouge' in value:
                    if 'rouge1' in value['rouge'] and not math.isnan(value['rouge']['rouge1']):
                        total_rouge1.append(value['rouge']['rouge1'])
                    if 'rouge2' in value['rouge'] and not math.isnan(value['rouge']['rouge2']):
                        total_rouge2.append(value['rouge']['rouge2'])
                    if 'rougeL' in value['rouge'] and not math.isnan(value['rouge']['rougeL']):
                        total_rougeL.append(value['rouge']['rougeL'])
            except (KeyError, TypeError, ValueError) as e:
                print(f"Error processing 'rouge' in {sub_key}: {e}")

            try:
                if 'meteor' in value and not math.isnan(value['meteor']):
                    total_meteor.append(value['meteor'])
            except (KeyError, TypeError, ValueError) as e:
                print(f"Error processing 'meteor' in {sub_key}: {e}")

            try:
                if 'bert' in value:
                    if 'Precision' in value['bert'] and not math.isnan(value['bert']['Precision']):
                        total_precision.append(value['bert']['Precision'])
                    if 'Recall' in value['bert'] and not math.isnan(value['bert']['Recall']):
                        total_recall.append(value['bert']['Recall'])
                    if 'F1' in value['bert'] and not math.isnan(value['bert']['F1']):
                        total_f1.append(value['bert']['F1'])
            except (KeyError, TypeError, ValueError) as e:
                print(f"Error processing 'bert' in {sub_key}: {e}")

    # Calculate averages, handle empty lists
    results = {
        'bleu4': round(np.mean(total_bleu4), 4) if total_bleu4 else float('nan'),
        'rouge1': round(np.mean(total_rouge1), 4) if total_rouge1 else float('nan'),
        'rouge2': round(np.mean(total_rouge2), 4) if total_rouge2 else float('nan'),
        'rougeL': round(np.mean(total_rougeL), 4) if total_rougeL else float('nan'),
        'meteor': round(np.mean(total_meteor), 4) if total_meteor else float('nan'),
        'bert': {
            'Precision': round(np.mean(total_precision), 4) if total_precision else float('nan'),
            'Recall': round(np.mean(total_recall), 4) if total_recall else float('nan'),
            'F1': round(np.mean(total_f1), 4) if total_f1 else float('nan')
        }
    }

    return results


# def ave_type_cate(metrics):
#     """
#     average_scores of each fq_type of each category

#     Para:::
#     metrics: dict of all scores of each fq_type of each category
#     """
#     results = {}
#     for key in metrics.keys():
#         total_bleu4 = []
#         total_rouge1 = []
#         total_rouge2 = []
#         total_rougeL = []
#         total_meteor = []
#         total_precision = []
#         total_recall = []
#         total_f1 = []

#         # Iterate over each entry in '0' and '1'
#         for sub_key in metrics[key]:
#             values = metrics[key][sub_key]
#             for value in values:
#                 if 'bleu4' in value:
#                     total_bleu4.append(value['bleu4'])
#                 if 'rouge' in value:
#                     total_rouge1.append(value['rouge']['rouge1'])
#                     total_rouge2.append(value['rouge']['rouge2'])
#                     total_rougeL.append(value['rouge']['rougeL'])
#                 if 'meteor' in value:
#                     total_meteor.append(value['meteor'])
#                 if 'bert' in value:
#                     total_precision.append(value['bert']['Precision'])
#                     total_recall.append(value['bert']['Recall'])
#                     total_f1.append(value['bert']['F1'])

#         # Calculate averages
#         results[key] = {
#             'bleu4': round(np.mean(total_bleu4), 4),
#             'rouge1': round(np.mean(total_rouge1), 4),
#             'rouge2': round(np.mean(total_rouge2), 4),
#             'rougeL': round(np.mean(total_rougeL), 4),
#             'meteor': round(np.mean(total_meteor), 4),
#             'bert': {
#                 'Precision': round(np.mean(total_precision), 4),
#                 'Recall': round(np.mean(total_recall), 4),
#                 'F1': round(np.mean(total_f1), 4)
#             }
#         }
    
#     return results