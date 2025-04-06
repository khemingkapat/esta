import pandas as pd


def downcast_df(df):
    for col, col_type in df.dtypes.items():
        str_type = str(col_type)
        if str_type.startswith("int"):
            df[col] = pd.to_numeric(df[col], downcast="integer")
        elif str_type.startswith("float"):
            df[col] = pd.to_numeric(df[col], downcast="float")
        elif col_type == "object" and df[col].nunique() <= (len(df) // 5):
            df[col] = df[col].astype("category")
    return df
