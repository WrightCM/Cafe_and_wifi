cafes = [1,2,3,4,5,6,7,8,9,10,11,12]
a = 0
for i in x:
    if a < 4:
        print(i)
        a += 1
    else:
        print('new row\n=========')
        print(i)
        a = 1

for cafe in cafes:
    if a < 4:
        print(cafe)