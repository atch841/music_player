import os
from config import LOG

def log(log_text):
    if os.path.exists(LOG):
        with open(LOG, 'r') as file:
            lines = file.readlines()
    else:
        lines = []

    if len(lines) > 50:
        lines = lines[-50:]

    lines.append(log_text + '\n')

    with open(LOG, 'w') as file:
        file.writelines(lines)

def read_log():
    if os.path.exists(LOG):
        with open(LOG, 'r') as file:
            lines = file.readlines()
    else:
        lines = ['']
    return "".join(lines)
