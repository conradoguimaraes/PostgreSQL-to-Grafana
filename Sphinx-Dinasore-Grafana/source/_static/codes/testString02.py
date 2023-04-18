k = 5
with open(path, "a+") as f:
    if (event_input_value % k == 0):
        f.write(data + "\n")
    else:
        f.write(data + ",")