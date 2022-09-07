import names, pdb, csv, sys, os


nameList = []
maxNames = int(sys.argv[1])

if os.path.exists(".\\fakeNames.csv"):
    os.remove(".\\fakeNames.csv")


def gen_Name(maxNames):
    row = 1
    # pdb.set_trace()
    while len(nameList) < maxNames:
        nameL = names.get_last_name()
        nameF = names.get_first_name()
        full_Name = (nameF +' '+ nameL)
        if full_Name not in nameList:
            nameList.append(nameF +' '+ nameL)
            writeNames_to_CSV(row,nameF,nameL)
            row +=1
            print(full_Name)
            continue
        else:
            continue


def writeNames_to_CSV(row,first,last):
    with open('.\\fakeNames.csv',mode='a',newline='') as fakeNames:
        csv_writer = csv.writer(fakeNames, delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([row,first,last])


gen_Name(maxNames)
print(len(nameList))





