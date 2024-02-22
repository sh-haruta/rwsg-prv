import argparse
import json

""" json template
{"root":
  {
    "title": "hoge1",
    "author": ["author a", "author b"],
    "abstract": "fuga",
    "introduction": "hogehoge",
    "relatedwork": "fugafuga"},
  "leaves":
   [
     {
       "title": "hoge1",
       "author": ["author a", "author b"],
       "year": 1111,
       "abstract": "fuga",
       "introduction": "hogehoge",
       "charge":  true
     },
     {
       "title": "hoge2",
       "author":["author a", "author b", "c"] ,
       "year": 1234,
       "abstract": "fuga",
       "introduction": "hogehoge",
       "charge": false }
  ]
}
"""


def add_alphabet(lst):
    seen = {}
    result = []

    for element in lst:
        if element not in seen:
            seen[element] = 1
            result.append(element)
        else:
            seen[element] += 1
            result.append(f"{element}{chr(ord('a') + seen[element] - 1)}")

    for i, item in enumerate(result):
        if item.endswith('b'):
            target = item[:-1]
            try:  # TODO: 重要なエラーをスキップしてしまいそう
                index = result.index(target)
                result[index] = target + 'a'
            except:
                pass

    return result


def process_root_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        root_info = json.load(f)['root']
    author_names = ""
    for a in root_info['author']:
        author_names += f"{a}, "
    author_names = author_names[:-2]

    title = f"[Your Title: \n{root_info['title']}\n]\n\n"
    intro = f"[Your Introduction: \n{root_info['introduction']}\n]\n\n"
    root_body = f'{title}{intro}'

    return root_body


def process_leaves_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        leaves_info = json.load(f)['leaves']
    first_author_list = []
    year_list=[]
    full_author_list = []
    for leaf in leaves_info:
        full_author_list.append(", ".join(leaf['author']))
        first_author_list.append(leaf['author'][0])
        year_list.append(leaf['year'])

    cite_name_list=[]
    for first_author, year in zip(first_author_list,year_list):
        cite_name_list.append(f"{first_author.split()[-1]} et al., {year}")

    cite_name_list = add_alphabet(cite_name_list)

    leaves_body = ''
    for i, leaf in enumerate(leaves_info):
        title = f"Title: {leaf['title']}\n"
        full_author = f"Authors: {full_author_list[i]}\n"
        citation_name = f"Citation Name: {cite_name_list[i]}\n"
        leaf_intro_flatten = leaf['introduction'].replace('\n', ' ')
        intro = f"Introduction: {leaf_intro_flatten}\n\n"
        if leaf['introduction'] == '':
            if leaf['abstract'] == '':
                raise Exception(f'At least abstract is needed.\n '
                                f'{full_author}{title}')
            intro = f"Introduction: {leaf['abstract']}\n\n"
        leaf_body = f'{title}{full_author}{citation_name}{intro}'
        leaves_body += leaf_body

    return leaves_body[:-1]
