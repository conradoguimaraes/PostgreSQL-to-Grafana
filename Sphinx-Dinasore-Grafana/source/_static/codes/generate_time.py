def generate_time(params_str):
    params = list(eval(params_str))
    t = round(np.random.normal(params[0], params[1]))
    return t


generate_time('10,2') #mu=10, std=2
#or
mu = 10 #Mean of the distribution.
std = 2 #Standard deviation of the distribution.
generate_time('mu,std')