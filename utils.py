import json


def load_api_key():
    with open('./env.local', 'r') as f:
        api_key = f.read().strip().split('OPENAI_API_KEY=')[1]
    return api_key


def load_org_id():
    with open('./env.local.org', 'r') as f:
        org_id = f.read().strip().split('OPENAI_ORG=')[1]
    return org_id


def select_prompt(prompt_file):
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt = f.read()
    return prompt


def get_paper_json(json_path):
    with open(f'{json_path}', 'r') as f:
        data = json.load(f)
    return data
