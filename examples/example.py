from generate import inf_csv

with open("example.csv", "r") as c:
    data = inf_csv(c, header=True)
    for _ in range(4):
        print(next(data))

# ['1', '2', '3']
# ['4', '5', '6']
# ['7', '8', '9']
# ['1', '2', '3']
