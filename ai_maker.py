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

def start_manufacture(client: openai.OpenAI, iteration: int, callback: Callable[[str], None]): 
   
    def create_chat(prompt: str):
            return client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompt},
                ])

    def manufacture(roles: list, current_iteration: int, last_feedback: str):
       def acc_builder(acc, role):
           if role is Thinker:
               prompt = role.generate_prompt(last_feedback)
               chat = create_chat(prompt)
               plan = get_response(chat)

               new_acc = acc + plan 
               callback(new_acc)
               return new_acc
           else: 
               prompt = role.generate_prompt(acc)
               chat = create_chat(prompt)
               response = get_response(chat)
               callback(response)
               return acc + get_response(chat)
           
       if current_iteration == iteration + 1:
           return 
       else: 
           result = reduce(acc_builder, roles, "")
           callback(result)
           manufacture(roles, current_iteration + 1, result)

    manufacture(load_roles_from_file("prompts.txt"), 1, "")
               

def test():
    client = pipe("api_key.txt", read_api_key, get_client)

    start_manufacture(client, 1, print)

test()

