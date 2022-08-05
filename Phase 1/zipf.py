import math
import pickle
import matplotlib.pyplot as plt

f = open("dict2.txt", "rb")
positional_dict = pickle.load(f)

edit_dict = {}
for key, value in positional_dict.items():
    edit_dict[key] = value.all_number_of_repetition

edit_dict = {k: v for k, v in sorted(edit_dict.items(), key=lambda item: item[1], reverse=True)}

edit_dict_keys = list(edit_dict.keys())
edit_dict_values = list(edit_dict.values())

max_number = edit_dict_values[0]

l = []
l2 = []
l3 = []
for i in edit_dict_values:
    l3.append(math.log(i, 10))

for i in range(len(edit_dict_keys)):
    l.append(math.log(i+1, 10))
    l2.append(math.log(max_number/(i+1), 10))

plt.plot(l, l2)
plt.plot(l, l3)
plt.show()
