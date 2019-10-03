import random
import string

def generate_random_string_with_numbers(min, max):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(min, max))])

def generate_random_string(min, max):
    return ''.join([random.choice(string.ascii_letters) for _ in range(random.randint(min, max))])

def generate_random_number(min, max):
    return ''.join([random.choice(string.digits) for _ in range(random.randint(min, max))])
