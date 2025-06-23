import random
import pathlib
import string
from typing import Callable
from sys import argv


"""
    This script aims to ease creation of env files.
    
    Usage:
    python generate_env_file.py [generate/touch/example]
    
    python generate_env_file.py :
       Creates a cli dialog to create .env file.
    
    python generate_env_file.py generate :
       Generates .env file using predefined rules.
    
    python generate_env_file.py touch :
       If .env file is not present, .env file will be generated
    
    python generate_env_file.py example :
       Generates an example env file
    
"""


class EnvCreatorRule:

    def __init__(self, creator_prompt: str, value_generator: Callable[[], str] | str):
        self._prompt = creator_prompt
        if isinstance(value_generator, str):
            self._value_generator = lambda: value_generator
        else:
            self._value_generator = value_generator

    def prompt(self) -> str:
        value = input(self._prompt)

        if len(value) == 0:
            value = self._value_generator()

        return value

    def generate(self):
        return self._value_generator()


def create_env_file(path: pathlib.Path, variables):

    with open(path, "w") as file:
        for var, value in variables.items():
            if '=' in var:
                raise ValueError()
            file.write(f"{var}={value}\n")


def generate_env_file(path: pathlib.Path, rules: dict[str, EnvCreatorRule], manual_mode=False):
    pairs: dict[str, str] = dict()

    for env, rule in rules.items():
        if manual_mode:
            pairs[env] = rule.prompt()
        else:
            pairs[env] = rule.generate()

    create_env_file(path, pairs)


def pass_gen() -> str:
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(20))


db_env_rules = {
    "DB_USER":          EnvCreatorRule("Enter db user [user]", 'user'),
    "DB_PASSWORD":      EnvCreatorRule("Enter db password [generate random]", pass_gen),
    "DB_NAME":          EnvCreatorRule("Enter db name [my-db]", 'my-db'),
    "DB_HOST":          EnvCreatorRule("Enter db host [db]", "db"),
    'DB_PORT':          EnvCreatorRule("Enter db port [5432]", '5432')
}


if __name__ == '__main__':
    db_env = pathlib.Path("env/db_env.env")
    if len(argv) < 2:
        generate_env_file(db_env, db_env_rules, True)
    elif argv[1] == 'generate':
        generate_env_file(db_env, db_env_rules)
    elif argv[1] == 'touch' and not db_env.exists():
        generate_env_file(db_env, db_env_rules)
    elif argv[1] == 'example':
        ex = pathlib.Path(db_env.__str__() + ".example")
        create_env_file(ex, {env: "..." for env, _ in db_env_rules.items()})

