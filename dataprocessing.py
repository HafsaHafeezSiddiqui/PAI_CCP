import pandas as pd

def input_dataframe(file_path, sort_by):
    # Read dataframe, sort it, and drop null values
    df = pd.read_csv(file_path)
    df = df.sort_values(by=sort_by)
    df = df.dropna()

    return df


def remove_outliers(df):
    for col in df.columns:
        # Calculate the maximum and minimum values for every column
        max = df[col].mean() + 3 * df[col].std()
        min = df[col].mean() - 3 * df[col].std()

        # Filter the DataFrame on max and min - removing outliers
        df = df[(df[col] > min) & (df[col] < max)]

    return df


if __name__ == '__main__':

    data_path = "data\\"

    sorting_keys = ['age', 'sex', 'cp']

    targetach = input_dataframe(data_path + "targetach.csv", sorting_keys)
    angina = input_dataframe(data_path + "angina.csv", sorting_keys)
    chol = input_dataframe(data_path + "chol.csv", sorting_keys)
    fbs = input_dataframe(data_path + "fbs.csv", sorting_keys)
    restbps = input_dataframe(data_path + "restbps.csv", sorting_keys)
    heartratemax = input_dataframe(data_path + "heartratemax.csv", sorting_keys)

    dataset_list = [angina, chol, fbs, restbps, heartratemax]

    # Treat targetach as main dataset which we will merge on, later
    targetach = remove_outliers(targetach)
    index = [i for i in range(int(targetach.size / len(targetach.columns)))]
    targetach.insert(0, "index", index)

    # Iterate through the individual data, clean it, and merge them into the main dataset
    for item in dataset_list:
        item = remove_outliers(item)
        item = item.drop(columns=sorting_keys, axis=0)
        index = [i for i in range(int(item.size / len(item.columns)))]
        item.insert(0, "index", index)
        targetach = pd.merge(targetach, item, on=['index'])
    print(targetach.head(50))