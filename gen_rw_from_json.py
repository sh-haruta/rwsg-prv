import os
from openai import OpenAI
from utils import load_api_key, load_org_id, select_prompt
from generate_root_leaves_prompt import process_root_info, process_leaves_info
import argparse

client = OpenAI(
    api_key=load_api_key(),
    organization=load_org_id()
)


def main(root_json_name):
    print(root_json_name)
    prompt_name = "generate_rws.txt"
    system_prompt = select_prompt(f'prompts/{prompt_name}')
    dir_dataset = 'dataset/jsons/'
    out_dir = 'dataset/results/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        print(f'{out_dir} is created.')

    # adjusting data
    root_paper = f'{dir_dataset}{root_json_name}.json'
    out_file = os.path.basename(root_paper).split('.')[0] + \
               f"{prompt_name.split('.')[0]}.txt"
    root_body = process_root_info(root_paper)
    leaves_body = process_leaves_info(root_paper)  # leaf info is in root json

    if args.pure_gpt:
        user_prompt = select_prompt(f'prompts/pure_generate_rws.txt') + \
                     f'\n\n {root_body}' + \
                     f'[Information about Related Studies:\n{leaves_body}]\n\n'
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0
        )
        print(response.choices[0].message.content)
        # save result
        with open(out_dir + os.path.basename(root_paper).split('.')[0] +
                  '_pure_gpt.txt', 'w', encoding='utf-8') as f:
            f.write(response.choices[0].message.content)
    else:
        user_prompt = f"For the following case, present your Results of " \
                      f"Step-2, and then proceed to write your Related Work " \
                      f"section.\n <Great case>\n {root_body}[Information " \
                      f"about Related Studies:\n{leaves_body}]\n\n"

        print(system_prompt)
        print(user_prompt)
        print(len(system_prompt.split()) + len(user_prompt.split()))

        response = client.chat.completions.create(
            model="gpt-4-1106-preview",  # gpt4-turbo for much input
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0
        )
        print(response.choices[0].message.content)
        # save result
        with open(out_dir + out_file, 'w', encoding='utf-8') as f:
            f.write(response.choices[0].message.content)


if __name__ == '__main__':
    # usage example python gen_rw_from_json.py --root_json_name 10
    parser = argparse.ArgumentParser(description='description')
    parser.add_argument('--root_json_name', type=str, help='json number')
    parser.add_argument('--pure_gpt', action='store_true')
    args = parser.parse_args()

    main(args.root_json_name)
