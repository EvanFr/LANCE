
from iocsearcher.searcher import Searcher
import csv
from openai import OpenAI
import json
import fitz  # PyMuPDF
import sys
import os
import glob
import tqdm


api_key = os.getenv("OpenAI_API_KEY")

searcher = Searcher()
client = OpenAI(api_key=api_key)

cap = 8000

GPT2IoC_searcher = {
            "IP": ["ip4"],
            "URL": ["url"],
            "HASH": ["sha256","sha1","md5"],
            "domain": ["fqdn"],
            "CVE": ["cve"]
        }

ResultsGPT_all = {
    "IP"    : {"TP":0,"FP":0,"FN":0},
    "CVE"   : {"TP":0,"FP":0,"FN":0},
    "hash"  : {"TP":0,"FP":0,"FN":0},
    "URL"   : {"TP":0,"FP":0,"FN":0},
    "domain": {"TP":0,"FP":0,"FN":0},
}
ResultsGPTstats_all = {
    "IP"    : {"Precision": {},"Recall": {}},
    "CVE"   : {"Precision": {},"Recall": {}},
    "hash"  : {"Precision": {},"Recall": {}},
    "URL"   : {"Precision": {},"Recall": {}},
    "domain": {"Precision": {},"Recall": {}},
}
ResultsIoC_searcher_all = {
    "ip4"   : {"TP":0,"FP":0,"FN":0},
    "cve"   : {"TP":0,"FP":0,"FN":0},
    "hashes": {"TP":0,"FP":0,"FN":0},
    "url"   : {"TP":0,"FP":0,"FN":0},
    "fqdn"  : {"TP":0,"FP":0,"FN":0}
}

Ground_Truth2GPT = {
    "IPv4"              :"IP",
    "CVE"               :"CVE",
    "FileHash"          :"hash",
    "URL"               :"URL",
    "domain"            :"domain",
}
Ground_Truth2AV = {
    "IPv4"              :"IPv4",
    "CVE"               :"CVE",
    "FileHash"          :"FileHash",
    "URL"               :"URL",
    "domain"            :"domain",
}
Ground_Truth2IoC_searcher = {
    "IPv4"              :"ip4",
    "CVE"               :"cve",
    "FileHash"          :"hashes",
    "URL"               :"url",
    "domain"            :"fqdn",
}

"""
File stracture Creation
"""

import os

current_path = os.getcwd()

# Create the directory for the txt of the reports
os.makedirs(current_path + "/ReportsTXT", exist_ok=True)

# Create the directory for the IoCs form IoC_searcher
os.makedirs(current_path + "/IoC_searcher_IoCs", exist_ok=True)

# Create the directory for the IoC_searcher IoC dictionary
os.makedirs(current_path + "/IoC_searcher_IoC_dict", exist_ok=True)

# Create the directory for the IoCs form GPT
os.makedirs(current_path + "/GPT_IoCs", exist_ok=True)
# Create the directory for the diferent types of IoCs form GPT
os.makedirs(current_path + "/GPT_IoCs/IP", exist_ok=True)
os.makedirs(current_path + "/GPT_IoCs/URL", exist_ok=True)
os.makedirs(current_path + "/GPT_IoCs/HASH", exist_ok=True)
os.makedirs(current_path + "/GPT_IoCs/domain", exist_ok=True)
os.makedirs(current_path + "/GPT_IoCs/CVE", exist_ok=True)

# Create the directory for PDFs with the highlights
os.makedirs(current_path + "/output_PDFs", exist_ok=True)


report_source_dir = current_path + "/ReportsJSON"

plural = {
    "IP": "IPs",
    "URL": "URLs",
    "HASH": "HASHes",
    "domain": "domains",
    "CVE": "CVEs"
}

def GPTJustSum (JustList):
    
    # adds the original prompt to the messages
    messages = [ {"role": "system", 
                "content": """Given the following list of justifications for labeling an indicator as either IoC (indicator of compromise) or non-IoC, provide a single, concise summary that reflects the reasons for the chosen classification. Ensure that the summary clearly aligns with the consensus of the justifications"""
                }]
    
    messages.append(
        {"role": "user", "content": "Justifications: " + ','.join(JustList)},
    )

    chat = client.chat.completions.create(
        model="gpt-4o", 
        messages=messages,
        # temperature=0.2
    )

    reply = chat.choices[0].message.content
    return reply

def GPTreq (prompt, report_part, IoC_searcher_type, GPT_type, pulse):

    # adds the original prompt to the messages
    messages = [ {"role": "system", 
                "content": prompt
                }]
    
    # the report segment goes through the IoC_seracher
    rawIoCs = searcher.search_data(report_part)

    # the extracted IoC are cleared and put in the IoC array
    listIoCs = list(rawIoCs)
    if len(listIoCs) == 0:
        return
    IoCs = []
    IoCs_values = []
    for i in listIoCs:
        if( i.name in IoC_searcher_type): #"sha256","sha1","md5"
            if( i.name in ["url"] and any(char in i.value for char in "{}[]")):
                continue
            IoCs.append([i.name, i.value])
            IoCs_values.append(i.value)


    IoCs_string = ""
    for entrie in IoCs:
        IoCs_string = IoCs_string + entrie[1] + "\n"


    messages.append(
        {"role": "user", "content": "Report segment: " + report_part},
    )

    messages.append(
        {"role": "user", "content": "Extracted "+plural[GPT_type]+": \n" + IoCs_string},
    )


    chat = client.chat.completions.create(
        model="gpt-4o", 
        messages=messages,
        # temperature=0.2
    )
    
    reply = chat.choices[0].message.content
    # print(f"ChatGPT: {reply}")
    # print(len(reply))

    with open(current_path+"/GPT_IoCs/"+GPT_type+"/"+pulse+".txt", 'a') as outfile:
        for row in reply.split("\n"):
            # print(row)
            try:
                ioc = row.split(",")[0]
                lbl = row.split(",")[1]
            except:
                continue
            if ioc in IoCs_values:
                outfile.write(row)
                outfile.write("\n")

def comment_pdf(input_file:str, search_list, ioc_dict, pages:list=None, highlight_output: bool=True):
    
    search_list = sorted(search_list, key=lambda x: len(x[0]), reverse=True)
    
    matches_record = create_matches_record(search_list)

    full_path =  current_path+ "/ReportsPDF/"+input_file+".pdf"
    
    try:
        pdfIn = fitz.open(full_path)
    except Exception as e:
        error_message = f"Error opening file {full_path}: {e}"
        print(error_message)
        return
    # Matches .ipynb file <<START>>
    for pg,page in enumerate(pdfIn):
        pageID = pg+1
        # UX
        sys.stdout.write(f"\rScanning page {pageID}...")
        sys.stdout.flush()

        # If required to look in specific pages
        if pages and pageID not in pages:
            continue

        # Use the search_for function to find text
        for search_settings in search_list:
            IoC_clear, comment = search_settings[:2]
            if len(search_settings) > 2:
                justification = ','.join(search_settings[2:])

            else:
                justification = "No justification provided."
            color = None

            # if the value of oc_dict[IoC_clear] is a list, then we have to search for all the values in the list
            matched_values = []
            if IoC_clear not in ioc_dict:
                continue
            for ioc_value in ioc_dict[IoC_clear]:
                matched_values.extend(page.search_for(ioc_value))

            merged_mached_values = clean_up_matches(matched_values)
            if merged_mached_values:
                update_matches_record(matches_record, IoC_clear, merged_mached_values)
                if highlight_output:
                    highlight_text(merged_mached_values, IoC_clear,  page, color, comment, justification)
    # UX
    # sys.stdout.write("Done!")
    # Matches .ipynb file <<END>>
    
    # Save to output files
    if highlight_output:
        output_file = create_output_file(input_file, pdfIn)
    else:
        comment_name = "none"
        output_file = "none"
        pdfIn.close()
    
    
    # print(f"Scan complete: {input_file}")

def clean_up_matches(matched_values):
    # this function is used to merge the matched values that are close to each other
    # to avoid highlighting the same word multiple times
    merged_matches = []
    for match in matched_values:
        if not merged_matches:
            merged_matches.append(match)
        else:
            last_match = merged_matches[-1]
            if match[0] < last_match[2] + 1 and match[3] < last_match[3] + 3 and match[3] > last_match[3] -3:
                new_match = (last_match[0], last_match[1], match[2], match[3])
                merged_matches[-1] = new_match
            else:
                merged_matches.append(match)
    
    return merged_matches


def read_csv(list_filename_csv):
    try:
        with open(list_filename_csv, 'r') as csv_data:
            csv_reader = csv.reader(csv_data)
            search_list = [row for row in csv_reader]
        return search_list
    except Exception as e:
        print(f"Error reading CSV file {list_filename_csv}: {e}")
        sys.exit(1)

def create_matches_record(search_list):
   return {search[0]: 0 for search in search_list}

def update_matches_record(matches_record, word, match_values):
   matches_record[word] += len(match_values)

def highlight_text(matched_values, ioc,  page, color, comment, justification):
    colors = {
        'blue': [0, 0, 1],
        'light blue': [.22, .9, 1],
        'green': [.42, .85, .16],
        'light green': [.77, .98, .45],
        'yellow': [1, .82, 0],
        'light yellow': [.99, .96, .52],
        'orange': [1, .44, .01],
        'light orange': [1, .75, .62],
        'red': [.90, .13, .22],
        'light red': [1, .50, .62],
        'pink': [.64, .19, .53],
        'light pink': [.98, .53, 1]
    }
    
    for item in matched_values:
        # Highlight found text
        try:
            annot = page.add_highlight_annot(item)
        except Exception as e:
            print("Error adding highlight annotation:")
            print("itemm:")
            print(ioc)
            print("location:")
            print(item)
            print("Comment:")
            print(comment)
            print("Error:")
            print(e)
            continue
        if comment == "IoC":
            color = 'red'
        elif comment == "nonIoC":
            color = 'green'
        if color and color.lower() in colors:
            annot.set_colors(stroke=colors[color.lower()])
        # Add comment to the found match
        info = annot.info
        info["title"] = ioc
        info["content"] = comment + " : "+justification
        annot.set_info(info)
        annot.update(opacity=0.0)

def create_output_file(input_file, pdfIn):
  output_file = current_path + "/output_PDFs/" + input_file + "_Highlighter.pdf"
  pdfIn.save(output_file,garbage=3,deflate=True)
  pdfIn.close()
  return output_file

with open(current_path+"/logs.txt", 'w') as file:
    file.write("")

with open(current_path+"/logs.txt",'r') as txt:
    logs = txt.read()


excludeCount =  0
os.chdir(report_source_dir)


for filename in tqdm.tqdm(glob.glob("*.json")):

    pulse = filename[0:-5]

    if pulse in logs:
        continue


    with open(current_path+"/logs.txt",'a') as txt:
        txt.write(pulse) 



    """
    Text extraction from the given pulse
    """
    # open the json file
    with open(filename, "r") as file:
        pulse_data = json.load(file)

    report_text = pulse_data["plain_text"]
    
    # write the text in a txt file
    with open(current_path+'/ReportsTXT/'+pulse+'.txt', 'w') as f:
        f.write(report_text)
    
    """
    IoC_searcher Indicator extraction
    """

    # # get the IoC_searcher indicators from the ReportTXT
    # with open(current_path+'/ReportsTXT/'+pulse+'.txt', "r") as txtfile:
    #     report_text = txtfile.read()

    # extract raw IoCs from txt with IoC_searcher
    raw_IoC_searcher_IoCs = searcher.search_data(report_text)
    list_raw_IoC_searcher_IoCs = list(raw_IoC_searcher_IoCs)

    with open(current_path+"/logs.txt",'a') as txt:
        txt.write(" IoC_searcher IoC count: " + str(len(list_raw_IoC_searcher_IoCs)) + " ")


    # get clear IoCs
    IoC_searcher_IoCs = []
    for i in list_raw_IoC_searcher_IoCs:
        IoC_searcher_IoCs.append([i.name, i.value])


    # write the IoC_searcher IoCs in a csv file
    with open(current_path+'/IoC_searcher_IoCs/'+pulse+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(IoC_searcher_IoCs)

    """
    IoC_searcher IoC dictionary extraction
    """
    # # get the IoC_searcher indicators from the ReportTXT
    # with open(current_path+'/ReportsTXT/'+pulse+'.txt', "r") as txtfile:
    #     report_text = txtfile.read()

    # extract raw IoCs from txt with IoC_searcher
    raw_IoC_searcher_IoC_dict = searcher.search_raw(report_text)

    # get clear IoCs
    IoC_searcher_IoC_dict = {}
    for i in raw_IoC_searcher_IoC_dict:
        if i[0] in ["md5", "sha1", "sha256"]: 
            if i[1].casefold() in IoC_searcher_IoC_dict.keys():
                if i[3] not in IoC_searcher_IoC_dict[i[1].casefold()]:
                    IoC_searcher_IoC_dict[i[1].casefold()].append(i[3])
            else:
                IoC_searcher_IoC_dict[i[1].casefold()]=[i[3]]
        elif i[0] in ["cve"]:
            if i[1].casefold() in IoC_searcher_IoC_dict.keys():
                if i[3] not in IoC_searcher_IoC_dict[i[1].casefold()]:
                    IoC_searcher_IoC_dict[i[1].casefold()].append(i[3])
            else:
                IoC_searcher_IoC_dict[i[1].casefold()]=[i[3]]
        else:
            if i[1] in IoC_searcher_IoC_dict.keys():
                if i[3] not in IoC_searcher_IoC_dict[i[1]]:
                    IoC_searcher_IoC_dict[i[1]].append(i[3])
            else:
                IoC_searcher_IoC_dict[i[1]]=[i[3]]

    # write the IoC_searcher IoCs in a csv file
    with open(current_path+'/IoC_searcher_IoC_dict/'+pulse+'.json', 'w') as jsonfile:
        json.dump(IoC_searcher_IoC_dict, jsonfile)

    """
    GPT IoC extraction
    """

    prompts ={}

    # get prompts for GPT 
    with open(current_path+'/prompts.txt', 'r') as file:
        for line in file:
            GPT_type = line.split(":")[0]
            prompt = line.split(":")[1]

            prompts[GPT_type] = prompt

    len_count = 0
    report_part = ""

    for GPT_type in prompts:    
        with open(current_path+'/ReportsTXT/'+pulse+'.txt', 'r') as file:
            half_point = False
            row = file.readline()
            while row:
                leng = len(row)
                report_part = report_part + row
                len_count += leng

                if (len_count + leng > cap/2) & (half_point == False):
                    position = file.tell()
                    half_point = True

                if (len_count + leng > cap) :
                    GPTreq(prompts[GPT_type], report_part, GPT2IoC_searcher[GPT_type], GPT_type, pulse)
                    len_count = 0
                    report_part = ""
                    half_point = False
                    file.seek(position)

                row = file.readline()

            GPTreq(prompts[GPT_type], report_part, GPT2IoC_searcher[GPT_type], GPT_type, pulse)

    

    """
    Comparison of the extracted IoC labels
    """

    ResultsGPT = {
        "file"  : pulse[:13],
        "IP"    : {"TP":0,"FP":0,"FN":0},
        "CVE"   : {"TP":0,"FP":0,"FN":0},
        "hash"  : {"TP":0,"FP":0,"FN":0},
        "URL"   : {"TP":0,"FP":0,"FN":0},
        "domain": {"TP":0,"FP":0,"FN":0},
    }
    ResultsIoC_searcher = {
        "file"  : pulse[:13],
        "ip4"   : {"TP":0,"FP":0,"FN":0},
        "cve"   : {"TP":0,"FP":0,"FN":0},
        "hashes": {"TP":0,"FP":0,"FN":0},
        "url"   : {"TP":0,"FP":0,"FN":0},
        "fqdn"  : {"TP":0,"FP":0,"FN":0}
    }

    # load IoC_searcher IoCs
    IoC_searcher_data = []
    IoC_searcher_IoCs = []
    with open(current_path+'/IoC_searcher_IoCs/'+pulse+'.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] in ["md5", "sha1", "sha256"]: 
                if ["hashes",row[1].casefold()] not in IoC_searcher_data:
                    row[0] = "hashes"
                    row[1] = row[1].casefold() # make all caracters small
            elif row[0] in ["cve"]:
                if ["cve",row[1].casefold()] not in IoC_searcher_data:
                    row[1] = row[1].casefold() # make all caracters small
            IoC_searcher_data.append(row)
            IoC_searcher_IoCs.append(row[1])

    # load GPT IoCs
    GPT_data = []
    GPT_IoCs = []
    GPT_info = {"CVE":{},"URL":{},"domain":{},"IP":{},"HASH":{}}
    file = current_path+"/GPT_IoCs/CVE/" + pulse + ".txt"
    with open(file, 'r') as txtfile:
        for row in txtfile:
            row = row.replace("\n","")
            if row.replace(" ","") == "" :
                continue
            # if(justs):
            #     if row.split(",")[1] != "IoC":
            #         continue
            ioc = row.split(",")[0].casefold()
            lbl = row.split(",")[1]
            if ioc not in GPT_info["CVE"]:
                if lbl == "IoC":
                    GPT_info["CVE"][ioc] = {"IoC" : [','.join(row.split(',')[2:])], "nonIoC" : []}
                elif lbl == "nonIoC":
                    GPT_info["CVE"][ioc] = {"IoC" : [], "nonIoC" : [','.join(row.split(',')[2:])]}
            else:
                if lbl == "IoC":
                    GPT_info["CVE"][ioc]["IoC"].append(','.join(row.split(',')[2:]))
                elif lbl == "nonIoC":
                    GPT_info["CVE"][ioc]["nonIoC"].append(','.join(row.split(',')[2:]))
        for ioc in GPT_info["CVE"]:
            if len(GPT_info["CVE"][ioc]["IoC"]) >= len(GPT_info["CVE"][ioc]["nonIoC"]):
                GPT_data.append(["CVE",ioc])
                GPT_IoCs.append(ioc)
    file = current_path+"/GPT_IoCs/URL/" + pulse + ".txt"
    with open(file, 'r') as txtfile:
        for row in txtfile:
            row = row.replace("\n","")
            if row.replace(" ","") == "" :
                continue
            # if(justs):
            #     if row.split(",")[1] != "IoC":
            #         continue
            ioc = row.split(",")[0]
            lbl = row.split(",")[1]
            if ioc not in GPT_info["URL"]:
                if lbl == "IoC":
                    GPT_info["URL"][ioc] = {"IoC" : [','.join(row.split(',')[2:])], "nonIoC" : []}
                elif lbl == "nonIoC":
                    GPT_info["URL"][ioc] = {"IoC" : [], "nonIoC" : [','.join(row.split(',')[2:])]}
            else:
                if lbl == "IoC":
                    GPT_info["URL"][ioc]["IoC"].append(','.join(row.split(',')[2:]))
                elif lbl == "nonIoC":
                    GPT_info["URL"][ioc]["nonIoC"].append(','.join(row.split(',')[2:]))
        for ioc in GPT_info["URL"]:
            if len(GPT_info["URL"][ioc]["nonIoC"]) == 0 : # GPT_info["URL"][ioc]["IoC"] > 4*GPT_info["URL"][ioc]["nonIoC"]:
                GPT_data.append(["URL",ioc])
                GPT_IoCs.append(ioc)
    file = current_path+"/GPT_IoCs/domain/" + pulse + ".txt"
    with open(file, 'r') as txtfile:
        for row in txtfile:
            row = row.replace("\n","")
            if row.replace(" ","") == "" :
                continue
            # if(justs):
            #     if row.split(",")[1] != "IoC":
            #         continue
            ioc = row.split(",")[0]
            lbl = row.split(",")[1]
            if ioc not in GPT_info["domain"]:
                if lbl == "IoC":
                    GPT_info["domain"][ioc] = {"IoC" : [','.join(row.split(',')[2:])], "nonIoC" : []}
                elif lbl == "nonIoC":
                    GPT_info["domain"][ioc] = {"IoC" : [], "nonIoC" : [','.join(row.split(',')[2:])]}
            else:
                if lbl == "IoC":
                    GPT_info["domain"][ioc]["IoC"].append(','.join(row.split(',')[2:]))
                elif lbl == "nonIoC":
                    GPT_info["domain"][ioc]["nonIoC"].append(','.join(row.split(',')[2:]))
        for ioc in GPT_info["domain"]:
            if len(GPT_info["domain"][ioc]["IoC"]) >= len(GPT_info["domain"][ioc]["nonIoC"]):
                GPT_data.append(["domain",ioc])
                GPT_IoCs.append(ioc)
    file = current_path+"/GPT_IoCs/IP/" + pulse + ".txt"
    with open(file, 'r') as txtfile:
        for row in txtfile:
            row = row.replace("\n","")
            if row.replace(" ","") == "" :
                continue
            # if(justs):
            #     if row.split(",")[1] != "IoC":
            #         continue
            ioc = row.split(",")[0].split(":")[0]
            lbl = row.split(",")[1]
            if ioc not in GPT_info["IP"]:
                if lbl == "IoC":
                    GPT_info["IP"][ioc] = {"IoC" : [','.join(row.split(',')[2:])], "nonIoC" : []}
                elif lbl == "nonIoC":
                    GPT_info["IP"][ioc] = {"IoC" : [], "nonIoC" : [','.join(row.split(',')[2:])]}
            else:
                if lbl == "IoC":
                    GPT_info["IP"][ioc]["IoC"].append(','.join(row.split(',')[2:]))
                elif lbl == "nonIoC":
                    GPT_info["IP"][ioc]["nonIoC"].append(','.join(row.split(',')[2:]))
        for ioc in GPT_info["IP"]:
            if len(GPT_info["IP"][ioc]["IoC"]) >=  len(GPT_info["IP"][ioc]["nonIoC"]):
                GPT_data.append(["IP",ioc])
                GPT_IoCs.append(ioc)
    file = current_path+"/GPT_IoCs/HASH/" + pulse + ".txt"
    with open(file, 'r') as txtfile:
        for row in txtfile:
            row = row.replace("\n","")
            if row.replace(" ","") == "" :
                continue
            # if(justs):
            #     if row.split(",")[1] != "IoC":
            #         continue
            ioc = row.split(",")[0].casefold()
            lbl = row.split(",")[1]
            if ioc not in GPT_info["HASH"]:
                if lbl == "IoC":
                    GPT_info["HASH"][ioc] = {"IoC" : [','.join(row.split(',')[2:])], "nonIoC" : []}
                elif lbl == "nonIoC":
                    GPT_info["HASH"][ioc] = {"IoC" : [','.join(row.split(',')[2:])], "nonIoC" : []}
            else:
                if lbl == "IoC":
                    GPT_info["HASH"][ioc]["IoC"].append(','.join(row.split(',')[2:]))
                elif lbl == "nonIoC":
                    GPT_info["HASH"][ioc]["nonIoC"].append(','.join(row.split(',')[2:]))
        for ioc in GPT_info["HASH"]:
            if len(GPT_info["HASH"][ioc]["IoC"]) >= len(GPT_info["HASH"][ioc]["nonIoC"]):
                GPT_data.append(["hash",ioc])
                GPT_IoCs.append(ioc)
    
    GPT_all_list = []

    for type in GPT_info:
        for ioc in GPT_info[type]:
            if ioc in GPT_IoCs:
                GPT_all_list.append([ioc,"IoC",GPT_info[type][ioc]["IoC"]])
            else:
                GPT_all_list.append([ioc,"nonIoC",GPT_info[type][ioc]["nonIoC"]])

    """
    Sumarise the justifications
    """

    for IoC in GPT_all_list:
        IoC[2] = GPTJustSum(IoC[2])

    """
    Generate the PDF
    """

    with open(current_path+'/GPT_IoCs/'+pulse+'.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(GPT_all_list)
    
    comment_pdf(input_file=pulse, search_list=GPT_all_list, ioc_dict=IoC_searcher_IoC_dict, pages=None, highlight_output=True)

    with open(current_path+"/logs.txt",'a') as txt:
        txt.write(" PDF created ")
        txt.write("\n")




    