
from dateutil.relativedelta import relativedelta
import pandas as pd




def filter_time(df, days=0):
    last_day = df.index[0].date()
    start_day = last_day - relativedelta(days=days)
    # sort_index() - skips a warning
    df = df.sort_index().loc[start_day:last_day]
    return df


def count_medals(df_orig, column_name, year="Year", medal="Medal"):
    df_medals = df_orig.groupby([column_name, year, medal]).count()["ID"].reset_index()
    df_medals = df_medals.pivot(index=[column_name, year], columns="Medal", values="ID")
    df_medals.fillna(0, inplace=True)
    df_medals.reset_index(drop=False, inplace=True )
    df_medals["Total"] = df_medals["Bronze"] + df_medals["Gold"] + df_medals["Silver"]
    df_medals['Year']= pd.to_datetime(df_medals['Year'], format='%Y').dt.year
    df_medals.iloc[:, -4:] = df_medals.iloc[:, -4:].astype("int64")
    return df_medals