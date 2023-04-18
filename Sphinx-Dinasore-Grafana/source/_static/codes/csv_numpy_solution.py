myArray = np.array([1, 2, 3, 4, 5, 6])

x = np.array2string(myArray, separator=',')
print(x)
>> [1,2,3,4,5,6]

#or

x = np.array2string(myArray, separator=',')[1:-1]
print(x)
>> 1,2,3,4,5,6


#or if it is a List type variable

lista = myArray.tolist()
x = ' '.join(str(index)+"," for index in lista)[:-1]
print(x)
>> 1, 2, 3, 4, 5, 6

#or

x = ' '.join("'"+str(index)+"'," for index in lista)[:-1]
print(x)
>> '1', '2', '3', '4', '5', '6'


#all of the above cases:
print(type(x))
>> <class 'str'>