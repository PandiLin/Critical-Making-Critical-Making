from expression import Some, Nothing, Option, pipe
import random

class Role: 
    def __init__(self, description: str): 
        self.description = description

    def generate_prompt(self, last_input: str): 
        return f"{self.description}"
    
class Thinker(Role): 
    def __init__(self, description: str): 
        super().__init__(description)
        self.framework_theory = ["post_capitalism", "post_humanism", "post_modernism", "ecology", "psychology", "gender_theory",
                                 "psychology_of_healing", "psycho_analysis", "critical theory", "queer theory", "community healing", 
                                 "symbiosis"]
        
    def random_get_one_from_framework_theory(self): 
        return random.choice(self.framework_theory)
    
    def generate_prompt(self, last_input: str): 
        feedback = "based on the last feedback:" + last_input
        framework_articulation = "Given the frameworks of" + self.random_get_one_from_framework_theory() \
                                + "generate a comprehensive plan for a critical making project."
        return f"{feedback} {framework_articulation} {self.description}"

class Maker(Role): 
    def __init__(self, description: str): 
        super().__init__(description)
    
    def generate_prompt(self, last_input: str): 
        # framework theory
        plan_articulation = "Given the plan:" + last_input 
        return f"{plan_articulation} {self.description}"
    
class Assessor(Role): 
    def __init__(self, description: str): 
        super().__init__(description)
    
    def generate_prompt(self, last_input: str): 
        # framework theory
        plan_articulation = "Given the plan and execution" + last_input 
        return f"{plan_articulation} {self.description}"

def load_roles_from_file_recursive(file):

    def set_description(role: str, description: str):
        match role: 
            case "THINKER": 
                return Thinker(description)
            case "MAKER": 
                return Maker(description)
            case "ASSESSOR": 
                return Assessor(description)

    def lc(file, roles: list, current_role: Option[str], description: str):
        line = file.readline()
        if line == "":
            if current_role is None:
                return roles
            else:
                roles.append(set_description(current_role, description))
                return roles
        if line.strip() in ['THINKER', 'MAKER', 'ASSESSOR']:
            if current_role is None:
                return lc(file, roles, line.strip(), description)
            else:
                roles.append(set_description(current_role, description))
                return lc(file, roles, line.strip(), "")
        else:
            description += line.strip() + " "
            return lc(file, roles, current_role, description)

    return lc(file, roles=[], current_role=None, description="")

def load_roles_from_file(file_path: str = 'prompts.txt'):
    with open(file_path, 'r') as file:
        return load_roles_from_file_recursive(file)
    
# result = load_roles_from_file()
# for role in result: 
#     print(role.description)
