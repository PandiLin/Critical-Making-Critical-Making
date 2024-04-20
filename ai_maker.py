import os 
import openai
from expression import pipe
from dataclasses import dataclass
from role import load_roles_from_file
from typing import Callable
from role import Role, Thinker, Maker, Assessor
from functools import reduce

def read_api_key(filename: "api_key.txt") -> str:
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found")

    with open(filename, "r") as file:
        return file.read().strip()


def get_client(api_key: str) -> openai.OpenAI:
    return openai.OpenAI(api_key=api_key)

def get_response(chat: openai.ChatCompletion) -> str:
    return chat.choices[0].message.content

def start_manufacture(last_feedback: str): 
    client = pipe("api_key.txt", read_api_key, get_client)
   
    def create_chat(prompt: str):
            return client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompt},
                ])
    
    def iter_on(roles, acc, last_feedback):
        m = lambda x: pipe(x, role.generate_prompt, create_chat, get_response)
        if not roles:
            raise Exception("No roles left")

        role = roles[0]
        if isinstance(role, Thinker):
            print("THINKING")
            return iter_on(roles[1:], m(last_feedback), last_feedback)
        elif isinstance(role, Maker):
            print("MAKING")
            return iter_on(roles[1:], acc + m(acc), last_feedback)
        elif isinstance(role, Assessor):
            print("ASSESSING")
            result = m(acc)
            return (acc + result, result)

    return iter_on(load_roles_from_file("prompts.txt"), "", last_feedback)

               

# def test():
#     client = pipe("api_key.txt", read_api_key, get_client)

#     start_manufacture(client, 1, print)

# test()

