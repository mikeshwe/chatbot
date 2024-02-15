import json
import jsonlines

# Load JSON file from local storage
def load_json_file(file_path):
    with open(file_path) as file:
        json_data = json.load(file)
    return json_data

# return an array of jsonl lines
def convert_to_jsonl(json_object):
    datalist = []
    system = {"role": "system", "content":"You are a friendly, professionial, and courteous chatbot assistant for Stanford Federal Credit Union (SFCU). You always answer in the first person singular (e.g., I, me, my ) or plural voice (e.g, we, our, us). I don't answer in the third person (e.g., they, them, theirs).  Your answers should demonstrate a brand voice that makes your customers feel Appreciated, Respected, and Valued.\
               The brand voice should also demonstrate the credit union's value of being a community partner and adapting to a customer's needs through their life time of events.."}
    
    for qa in json_object["prompt_response_pairs"]:
        question = qa["prompt"]
        answer = qa["response"]
        user = {"role":"user","content": question}
        assistant = {"role":"assistant","content": answer}
        row = {"messages":[system,user,assistant]}
        datalist.append(row)
    return datalist    

def write_jsonl_file(filepath,rowlist):
    with open(filepath, 'w') as out:
        for ddict in rowlist:
            jout = json.dumps(ddict) + '\n'
            out.write(jout)



def main():
   file_path = "docs/ft4_edited.json"  
   json_object = load_json_file(file_path)
   rowlist = convert_to_jsonl(json_object)
   write_jsonl_file('docs/sfcu_ft4.jsonl',rowlist)


if __name__ == "__main__":
    main()
