import json
import jsonlines
import csv

def load_tsv_file(tsv_file_path):
    datalist = []
    system = {"role": "system", "content":"I am an extremely friendly and courteous chatbot assistant for Stanford Federal Credit Union (SFCU). I always answer in the first person singular (e.g., I, me, my ) or plural voice (e.g, we, our, us). I don't answer in the third person (e.g., they, them, theirs). I always thank the customer for asking their question, and always thank them for being a member of Stanford FCU."}
    with open(tsv_file_path,encoding='latin-1') as file:
        tsv_reader= csv.reader(file, delimiter="\t")
        for row in tsv_reader:
            if len(row) >= 2:
                question = row[0].strip()
                answer = row[1].strip()
                datalist.append(answer)
    return datalist    

def write_csv_file(filepath,rowlist):
    with open(filepath, 'w') as out:
        for row in rowlist:
            out.write(row+"\n")



def main():
   file_path = "docs/sfcu_faq.tsv"  
   rowlist = load_tsv_file(file_path)
   write_csv_file('docs/sfcu_respones.csv',rowlist)


if __name__ == "__main__":
    main()
