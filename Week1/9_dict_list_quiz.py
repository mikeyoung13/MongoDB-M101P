obj = {'a':1,'b':2,'c':[1,3,5]}
sum = 0
if 'c' in obj:
    for n in obj['c']:
        sum = sum + n
print sum
