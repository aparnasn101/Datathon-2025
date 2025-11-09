with open("IngredientsUsed.csv", 'w') as newfile:
    with open("MSY Data - Ingredient.csv", "r") as myfile:
        linelist = [line.strip() for line in myfile]
        newfile.write(linelist[0] + '\n')
        for i in range(1, len(linelist)):
            fields = linelist[i].split(',')
            for j in range(len(fields)):
                if fields[j] == '':
                    fields[j] = '0'
            newfile.write(','.join(fields) + '\n')


# convert shipments to months

timedict = {"weekly": 4, "biweekly": 2, "monthly": 1}

with open("MonthlyShipments.csv", "w") as newfile:
    with open("MSY Data - Shipment.csv", "r") as myfile:
        linelist = [line.strip() for line in myfile]  # remove \n from each line

        # write header
        newfile.write("Ingredient,quantity\n")

        for line in linelist[1:]:
            item = line.split(',')
            name = item[0]
            quantity = float(item[1])
            multiplier1 = float(item[3])
            # get multiplier from timedict using the value in column 4
            freq = item[4].lower()  # ensure lowercase to match timedict keys
            multiplier2 = timedict.get(freq, 1)  # default to 1 if key not found

            total = quantity * multiplier1 * multiplier2

            # write to new file
            newfile.write(f"{name},{total}\n")

            





