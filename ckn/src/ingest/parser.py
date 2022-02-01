import pandas as pd

def parse_file(filename):
    df = pd.read_csv(filename)
    keys = df.keys()
    data = df.to_numpy()
    return data, keys

