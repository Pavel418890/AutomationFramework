import csv
import random
import string
from typing import Optional, List


def generate_random_string(length: int, char_type: Optional[str] = None) -> str:
    type_mapping = {
        'punctuation': string.punctuation,
        'digits': string.digits,
        'mix': string.ascii_letters + string.digits,
        'letters': string.ascii_letters,
    }
    chars = type_mapping.get(char_type) or ' '
    return ''.join(random.choice(chars) for _ in range(length))


def generate_random_email(
    local_length: int, domain_length: int,
    char_type_local: Optional[str] = None,
    char_type_domain: Optional[str] = None
) -> str:
    return '{0}{1}{2}{3}'.format(
        generate_random_string(local_length, char_type_local),
        '@',
        generate_random_string(domain_length, char_type_domain),
        '.com'
    )


def load_csv_data_as_nested_list(filename: str) -> List[list]:
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)
        return [line for line in reader]


