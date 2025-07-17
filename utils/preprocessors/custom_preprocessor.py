# Tokenizer
import re
import spacy
from utils.constants import FRAMEWORK_SPECIFIC_WORDS, LANGUAGE_SPECIFIC_WORDS

spacy_nlp = spacy.load('en_core_web_md')
spacy_nlp.max_length = 10000000

# preprocess： goes before the clustering
def custom_preprocess(text: str) -> str:
    stats = {
        'num_code_blocks': 0,
        'num_classes': 0,
        'num_camel_case': 0,
        'num_pascal_case': 0,
        'num_methods': 0,
        'num_ip_addresses': 0,
        'num_html_tags': 0,
        'num_links': 0,
        'num_user_mentions': 0,
        'num_numbers': 0,
        'num_special_characters': 0,
        'num_framework_specific_words': 0,
        'num_language_specific_words': 0
    }
    # TEXT BASED CHANGES
    # extract class and method names from code blocks, and remove the code blocks
    remove_multiline_code = re.compile(r"```[\s\S]*?```")
    code_blocks = re.findall(remove_multiline_code, text)
    for code_block in code_blocks:
        stats['num_code_blocks'] += 1
        # find classnames and method names
        classnames = re.findall(r'class [\w]+', code_block)
        methodnames = re.findall(r'[\w]+\(.*?\)', code_block)
        stats['num_classes'] += len(classnames)
        stats['num_methods'] += len(methodnames)
        # handle class and method naming schemes
        camel_case_pattern = re.compile(r'([a-z]+)([A-Z][a-z]+)+')
        pascal_case_pattern = re.compile(r'[A-Z][a-z]+')
        multiple_capitals_to_pascal_case_pattern = re.compile(r'^[A-Z]+[A-Z][a-z]+([A-Z][a-z]+)*$')

        new_class_method_names = []
        
        for name in classnames + methodnames:
            tokens = []
            # split where there is _, space, -, .
            tokens.extend(re.split(r'[_\-. ]', name)) 
            tokens_final = []
            # loop through each token
            for token in tokens:
                # if the token is a camel case
                if camel_case_pattern.match(token):
                    # split the camel case
                    stats['num_camel_case'] += 1
                    tokens_final.extend(re.findall(r'[A-Z][a-z]+', token))
                # if the token is a pascal case
                elif pascal_case_pattern.match(token):
                    # split the pascal case
                    stats['num_pascal_case'] += 1
                    tokens_final.extend(re.findall(r'[A-Z][a-z]+', token))
                elif multiple_capitals_to_pascal_case_pattern.match(token):
                    stats['num_pascal_case'] += 1
                    tokens_final.extend(re.findall(r'[A-Z][a-z]*', token))
                else:
                    tokens_final.append(token)

            new_class_method_names.append(' '.join(tokens_final))

    remove_singleline_code = re.compile(r"`[\s\S]*?`")
    code_blocks = re.findall(remove_singleline_code, text)
    for code_block in code_blocks:
        text = text.replace(code_block, '')

    # remove ip addresses
    find_ip_addresses = re.compile(r"((25[0-5]|2[0-4]\d|1\d{2}|\d{1,2}|xx)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|\d{1,2}|xx)")
    stats['num_ip_addresses'] += len(re.findall(find_ip_addresses, text))
    text = re.sub(find_ip_addresses, '', text)

    # remove html tags
    find_html_tags = re.compile(r'<.*?>')
    stats['num_html_tags'] += len(re.findall(find_html_tags, text))
    text = re.sub(find_html_tags, '', text)

    # delete links
    find_links = re.compile(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})")
    stats['num_links'] += len(re.findall(find_links, text))
    text = re.sub(find_links, '', text) 

    # remove user mentions
    find_user_mentions = re.compile(r'@[\w]+')
    stats['num_user_mentions'] += len(re.findall(find_user_mentions, text))
    text = re.sub(find_user_mentions, '', text)

    # remove numbers
    find_numbers = re.compile(r"\d+")
    stats['num_numbers'] += len(re.findall(find_numbers, text))
    text = re.sub(find_numbers, '', text)

    # remove special characters
    find_special_characters = re.compile(r"[^a-zA-Z0-9\s]")
    stats['num_special_characters'] += len(re.findall(find_special_characters, text))
    text = re.sub(find_special_characters, ' ', text)

    # remove framework and language specific words
    for word in FRAMEWORK_SPECIFIC_WORDS:
        # remove word from text regardless of case
        stats['num_framework_specific_words'] += len(re.findall(re.escape(word), text, re.IGNORECASE))
        text = re.sub(re.compile(re.escape(word), re.IGNORECASE), '', text)
    for word in LANGUAGE_SPECIFIC_WORDS:
        # remove word from text regardless of case
        stats['num_language_specific_words'] += len(re.findall(re.escape(word), text, re.IGNORECASE))
        text = re.sub(re.compile(re.escape(word), re.IGNORECASE), '', text)

    # ensure only one space between words
    text = re.sub(r'\s+', ' ', text)

    return text, stats

# tokenize: goes after the clustering
def tokenize(text: str) -> list[str]:
    # lowercase all words
    text = text.lower()
    # remove stop words and lemmatize
    text = spacy_nlp(text)
    tokens = [token.lemma_ for token in text if not token.is_stop and not token.is_punct and not token.is_space]

    return tokens