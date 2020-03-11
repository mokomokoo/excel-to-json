import sys
import pandas as pd
import re, json


def read_excel(file, header=[0, 0], columns=[0, 0]):
    df = pd.read_excel(file, encoding='GBK', sep=',', header=[header[0], header[1]])
    # print(df.iloc[:, columns[0]:columns[1]].head())
    # print(df.columns.values[columns[0]:columns[1]])

    data = df.iloc[:, columns[0]:columns[1]]
    headers = df.columns.values[columns[0]:columns[1]]

    new_headers = []
    for header in headers:
        header = list(header)
        new_columns = []
        for sub_header in header:
            if re.search('^Unnamed: \d+_level_\d+$', sub_header):
                continue
            new_columns.append(sub_header)
        new_headers.append(new_columns)

    new_json_header = []
    for header in new_headers:
        json_header = ".".join(header)
        new_json_header.append(json_header)

    data.columns = new_json_header

    with open('test.json', 'w+', encoding='GBK') as f:
        f.write('[')
        for index in data.index:
            f.write(data.loc[index].to_json())
            f.write(',\n') if not index == data.index[-1] else f.write(']')


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("please input the file name, header range (default 0 0 means only use the 0th row as header), "
              "wanted column range (default 0 0 means no column is selected), support negative number")
    else:
        read_excel(sys.argv[1], [int(sys.argv[2]), int(sys.argv[3])], [int(sys.argv[4]), int(sys.argv[5])])