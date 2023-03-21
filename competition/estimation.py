import csv
sort_list = ["nickname", "place", "ept points", "average", "offense", "defense", "versatility", "multitasking", "mechanics", "speed"]
final_list = []

with open('players.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    next(csvreader)
    sorted_data = sorted(csvreader, key=lambda row: float(row[9]))

summs_list = []

for i in range(1,10):
    summ = 0
    ind = 1
    print("The summ for:", sort_list[i])
    sorted_data.sort(key=lambda x: float(x[i]), reverse=True)
    for row in sorted_data:
        summ += (float(row[1])-float(ind))**2
        print(row[0] + " "  + str(row[1]) + " "  + str(ind) + " " + str(row[i]))
        ind += 1
    summs_list.append(summ)

for i in range(9):
    final_list.append(str(summs_list[i]) +  " --- " +  str(sort_list[i+1]))


final_list.sort()

for l in final_list:
    print(l)
