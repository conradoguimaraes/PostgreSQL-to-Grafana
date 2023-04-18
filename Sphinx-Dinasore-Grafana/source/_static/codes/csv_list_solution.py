lista = [1, 2, 3, 4, 5, 6]
' '.join(str(index)+"," for index in lista)[:-1]
>> '1, 2, 3, 4, 5, 6'

#or
' '.join("'"+str(index)+"'," for index in lista)[:-1]
>> "'1', '2', '3', '4', '5', '6'"