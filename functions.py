
# This function is made for analyzing and getting data that we need
 

def count_medals(df, *data):
    """
    Gives back number of medals groupby several attributes: *data
    and it returns a new DataFrame

    """
    #The special syntax *args is used to pass a variable number of arguments to a function. 
    #The syntax is to use the symbol * to take in a variable number of arguments based on the link: https://www.programiz.com/python-programming/args-and-kwargs
    # we start by removing all NaN in the column
    #https://trenton3983.github.io/files/projects/2019-02-04_manipulating_dataframes_with_pandas/2019-02-04_manipulating_dataframes_with_pandas.html
    df_medals = df[df['Medal'].notna()]
    
    #count medals by column
    datas_list = list(data)
    datas_list.append("Medal")
    df_medals = df_medals.groupby(datas_list).count().reset_index()

    #the sum of medals is listed in 'ID'
    datas_list.append("ID")
    df_medals = df_medals.loc[:, datas_list]
    
    # Changes dataframe from long to wide: Return reshaped DataFrame organized by given index / column values:https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot.html
    datas = list(data)
    df_medals = df_medals.pivot(index=datas, columns="Medal", values="ID")

    # fill out the missing values with a specified value which is 0
    df_medals.fillna(0, inplace=True)

    # declare Total
    df_medals["Total"] = df_medals["Gold"] + df_medals["Silver"] + df_medals["Bronze"]
    
    # modify columns and reset index(Lektion)
    df_medals = df_medals.astype(int).reset_index(inplace=False)

    
    return df_medals



