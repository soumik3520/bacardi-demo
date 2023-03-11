import pandas as pd


def read_data(file_name, separator=";"):
    df = pd.read_csv(file_name, sep=separator, encoding="ISO-8859-1")
    grp_cols = [
        "Retailer",
        "Category",
        "Segment",
        "Sub-Segment",
        "Brand",
        "KNAC-14",
        "Description",
        "Day",
        "Month",
        "Year",
    ]
    df = (
        df.groupby(grp_cols)
        .agg(Units=("Units", "sum"), Volume=("Sales in kg", "sum"))
        .reset_index()
    )
    df["Date"] = df[["Day", "Month", "Year"]].apply(
        lambda row: "-".join(row.values.astype(str)), axis=1
    )
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y").dt.normalize()
    df["SKU"] = df["Description"]
    df = df.drop(["Day", "Month", "Year", "Description"], axis=1)
    return df


tt = read_data("data/Weekly SO Data V2 WALMART.csv")
