import random
import string
import re
import os

def generate_random_string_with_numbers(min, max):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(min, max))])

def generate_random_string(min, max):
    return ''.join([random.choice(string.ascii_letters) for _ in range(random.randint(min, max))])

def generate_random_number(min, max):
    return ''.join([random.choice(string.digits) for _ in range(random.randint(min, max))])

def check_filename_is_same_on_model(model, base_path, filename, media_dir):
    filename, file_extension = os.path.splitext(filename)
    same_name = re.match(base_path + filename + ".*" + file_extension, model.image.name)
    return same_name

def check_file_exists_on_model(model, base_path, filename, media_dir):
    file_exists = os.path.isfile(media_dir + model.image.name)
    return file_exists
