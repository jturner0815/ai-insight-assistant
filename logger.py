import csv
from datetime import datetime
import os

def log_prompt(username, prompt, response, logfile='logs/prompts.csv'):
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    with open(logfile, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            writer.writerow(['timestamp', 'user', 'prompt', 'response'])
        writer.writerow([datetime.now().isoformat(), username, prompt, response])
