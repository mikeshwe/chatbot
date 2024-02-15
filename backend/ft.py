from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import os

_ = load_dotenv(find_dotenv()) # read the local .env file

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


fileObject = client.files.create(
    file=open("docs/sfcu_ft.jsonl", "rb"),
    purpose="fine-tune"
    )

# print (fileObject.id)


fineTuningJob = client.fine_tuning.jobs.create(
    training_file=fileObject.id,
    model = "gpt-3.5-turbo-1106"
    )

# print(client.fine_tuning.jobs.list(limit=10))
