import numpy as np

def generate_data(params_str, anom):
    params = list(eval(params_str))

    # generates the values
    sample = []
    print(params, "\n")
    for norm_param, anom_param in params:
        print("norm param: ", norm_param)
        print("anom_param: ", anom_param)
        # checks if an anomaly to generate
        if anom == 0:
            mu, std = norm_param
        else:
            if type(anom_param) == float:
                mu, std = anom_param, anom_param
            else:
                mu, std = anom_param

        # generates the value
        value = round(np.random.normal(mu, std), 3)

        # stores the value
        sample.append(value)

    # appends the anom at the end and converts it to string
    sample.append(anom)
    data_str = ','.join(['{0}'.format(x) for x in sample])
    return data_str



# generates data
ttf = 3
mtta = 5
anom = 1 if ttf <= mtta else 0

#tuple: (norm_param1, anom_param1)
data_str = generate_data("[\
                            (-1.0, 0.5), \
                            (2.0, 1.0), \
                            (10.0, 0.1), \
                            (3.0, 1.0)\
                          ]", anom)
print(data_str)

>> norm param:  -1.0
>> anom_param:  0.5

>> norm param:  2.0
>> anom_param:  1.0

>> norm param:  10.0
>> anom_param:  0.1

>> norm param:  3.0
>> anom_param:  1.0

>> 0.617,1.482,0.097,2.688,1
