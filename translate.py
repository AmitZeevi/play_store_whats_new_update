import csv
import pandas as pd
import os

def excel_to_csv(path):
    wb = pd.ExcelFile(path)

    try:
        spaces_sheet = pd.read_excel(wb, 'spaces')
        owner_sheet = pd.read_excel(wb, 'owner')
    except:
        print("The Excel sheet is not in the right format, talk to production team")
        

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
      
def main():
    path = input("please insert the Excel name: ")
    excel_to_csv(path)

    spaces_map = csv_to_map('spaces_trans.csv')
    owner_map = csv_to_map('owner_trans.csv')

    map_to_file('owner_default.txt', owner_map)
    map_to_file('spaces_default.txt', spaces_map)
    print('File created succecfully, you can find it in "files_to_upload" folder')

    os.remove('spaces_trans.csv')
    os.remove('owner_trans.csv')

if __name__ == '__main__':
    main()



