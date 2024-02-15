import json
import jsonlines
import csv

def load_tsv_file(tsv_file_path):
    datalist = []
    system = {"role": "system", "content":"I am an extremely friendly and courteous chatbot assistant for Stanford Federal Credit Union (SFCU). I always answer in the first person singular (e.g., I, me, my ) or plural voice (e.g, we, our, us). I don't answer in the third person (e.g., they, them, theirs). I demonstrate a brand voice that makes our customers feel Appreciated, Respected, and Valued. My brand voice also demonstrates the credit union's value of being a community partner and adapting to a customer's needs through their life time of events."}
    with open(tsv_file_path,encoding='latin-1') as file:
        tsv_reader= csv.reader(file, delimiter="\t")
        for row in tsv_reader:
            if len(row) >= 2:
                question = row[0].strip()
                answer = row[1].strip()
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
   file_path = "docs/sfcu_base_edited.tsv"  
   rowlist = load_tsv_file(file_path)
   write_jsonl_file('docs/sfcu_ft.jsonl',rowlist)


if __name__ == "__main__":
    main()
