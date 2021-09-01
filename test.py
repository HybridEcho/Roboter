import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])
c = np.concatenate((a, b), axis=0)
print(c)


combined_csv=np.array([[1,2], [5,6], [10,11]])
combined=np.array([[3,4]])

combined_csv= np.concatenate((combined_csv, combined), axis=0)

print(combined_csv)