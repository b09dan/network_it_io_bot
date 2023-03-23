import csv
import numpy as np
from scipy.stats import pearsonr, spearmanr

def parse_csv(file_name):
    result = {}
    with open(file_name, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        headers = next(reader)
        for index, header in enumerate(headers):
            result[header] = []

        #dict with list of lists
        for row_num, row in enumerate(reader, start=1):
            for col_num, value in enumerate(row):
                result[headers[col_num]].append((row_num, float(value)))
        #sort all by value
        for header in headers:
            if "place" in header:
                result[header].sort(key=lambda x: x[1])
            else:
                result[header].sort(key=lambda x: x[1], reverse=True)

    return result

def calculate(parsed_csv):
    list_result = []
    for key in parsed_csv:
        if "nickname" not in key:
            places_array = np.array([float(item[0]) for item in parsed_csv[key]])
            values_array = np.array([float(item[1]) for item in parsed_csv[key]])
            rangs_array = np.array([index + 1 for index, _ in enumerate(parsed_csv[key])])

            pearson_corr, pearson_p = pearsonr(places_array, values_array)
            spearman_corr, spearman_p = spearmanr(places_array, rangs_array)

            list_result.append([key, round(pearson_corr,2), round(pearson_p,2), round(spearman_corr, 2), round(spearman_p, 2)])
            #print(places_array)
            #print(values_array)
            #print(rangs_array)

    return list_result

## main
list_result = []
file_name = 'data/players.csv'

parsed_csv = parse_csv(file_name)
list_result = calculate(parsed_csv)

list_result.sort(key=lambda x: x[3], reverse=True)        
for elem in list_result:
    print(elem)

