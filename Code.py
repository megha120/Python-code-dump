from os import listdir
import argparse
import csv

def main(args):
    path = args.folder_path
    row_list = [["FileName", "Start", "End","Count"]]
    for f in listdir(path):
        file_path=path+"/"+f
        fileName = f.replace('_pause.txt','')
        with open (file_path, "r") as myfile:
            data = myfile.read().replace('\n', '')
            if len(data)>2:
                ls = data.split('), ')
                count = len(ls)
                for j,i in enumerate(ls):
                    ls2 = i.split(',')
                    start = ls2[0].replace('[(','').replace('(','').replace("'", '')
                    end = ls2[1].replace(' ','').replace(')]','').replace("'", '')
                    if j==0:
                        row_list.append([fileName,start,end,count])
                    else:
                        row_list.append(['',start,end,''])
        
    print(row_list)
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating a csv')
    parser.add_argument('--folder_path', metavar='path', required=True, help='the path to workspace')
    args = parser.parse_args()
    main(args)