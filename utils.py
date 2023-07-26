from config import LOG

def log(log_text):
    with open(LOG, 'r') as file:
        lines = file.readlines()

    if len(lines) > 50:
        lines = lines[-50:]

    lines.append(log_text + '\n')

    with open(LOG, 'w') as file:
        file.writelines(lines)

def read_log():
    with open(LOG, 'r') as file:
        lines = file.readlines()
    return "".join(lines)
