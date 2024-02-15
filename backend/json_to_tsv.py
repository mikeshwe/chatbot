import json
import jsonlines

# Load JSON file from local storage
def load_json_file(file_path):
    with open(file_path) as file:
        json_data = json.load(file)
    return json_data

# return an array of jsonl lines
def convert_to_tsv(json_object):
    datalist = []
    
    for qa in json_object["training_examples"]:
        question = qa["prompt"]
        answer = qa["response"]
        row = {"question":question,"answer":answer}
        datalist.append(row)
    return datalist    

def write_tsv_file(filepath,rowlist):
    with open(filepath, 'w') as out:
        out.write("PROMPT\t"+"RESPONSE\n")
        for row in rowlist:
            out.write(row["question"]+"\t"+row["answer"]+"\n")

def main():
   file_path = "docs/ft3.json"  
   json_object = load_json_file(file_path)
   rowlist = convert_to_tsv(json_object)
   write_tsv_file('docs/sfcu_ft3.tsv',rowlist)


if __name__ == "__main__":
    main()
