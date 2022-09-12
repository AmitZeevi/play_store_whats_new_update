import csv
from logging import error
import pandas as pd
import os.path
from os import path

#TODO
# file picker instead of path
# radio buttons for -spaces -owner
# google integration

def excel_to_csv(wb):
    spaces_sheet = pd.read_excel(wb, 'spaces')
    owner_sheet = pd.read_excel(wb, 'owner')
      
    spaces_sheet.to_csv('owner_trans.csv', index=False)
    owner_sheet.to_csv('spaces_trans.csv', index=False)

def csv_to_map(filename) -> map:

    lang = []
    rows = []

    with open(filename, 'r', encoding='utf-8-sig') as csvfile:
        csvreader = csv.reader(csvfile)
        
        lang = next(csvreader)        
    
        for i, row in enumerate(csvreader):
            rows.append(row)
            if i == 1:
                break
        translations = rows[1]
    
    # lang to lower case, w/o spaces 
    for i in range(len(lang)):
        lang[i] = lang[i].lower().strip()

    map = {}

    for i in range(len(lang)):
        map[lang[i]] = translations[i]+'\n'
    return map
    
def map_to_file(filename, translations):
     with open(filename, 'r') as f:
        lines = f.readlines()

        for i in range(len(lines) // 3):
            lang_code = lines[3*i][1:3]

            if lang_code in translations:
                lines[3*i +1] = translations[lang_code]
            else:
                # Default language 
                lines[3*i +1] = translations['en']
        output = filename.split("_")[0]+"_to_store.txt"
        output = "./files_to_upload/"+output
        with open(output,'w') as output_file:
            output_file.writelines(lines)
      
def path_validation(src):
    if not path.exists(src):
        raise error()

def main():
    path = input("please insert the Excel name: ")
    
    # Validate file exists and .xlsx
    try:
        path_validation(path)
        wb = pd.ExcelFile(path)
    except:
        print("path is invalid. Format exepted is .xlsx only")
        return

    # Validate sheets name are correct
    try:
        excel_to_csv(wb)
    except:
        print("The Excel sheet is not in the right format, talk to production team")
        return

    spaces_map = csv_to_map('spaces_trans.csv')
    owner_map = csv_to_map('owner_trans.csv')

    map_to_file('owner_default.txt', owner_map)
    map_to_file('spaces_default.txt', spaces_map)
    print('File created succecfully, you can find it in "files_to_upload" folder')

    os.remove('spaces_trans.csv')
    os.remove('owner_trans.csv')
    # upload to google console
    


if __name__ == '__main__':
    main()



