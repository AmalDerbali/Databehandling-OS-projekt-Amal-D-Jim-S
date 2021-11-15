import pandas as pd

df = pd.read_csv("C:/Users/Amal Derbali/Documents/GitHub/Databehandling-OS-projekt-Amal-D-Jim-S/Data/athlete_events.csv")
print(df.head())

class StockDataLocal:
    """Class method to get and process local stock data"""
    def __init__(self, data_folder_path: str = "C:/Users/Amal Derbali/Documents/GitHub/Databehandling-OS-projekt-Amal-D-Jim-S/Data") -> None:
        self._data_folder_path = data_folder_path
    
    def stock_dataframe(self, stockname: str) -> list:
        """
        Returns:
            list of two dataframes, one for daily time series, one for interdaily
        """
        stock_df_list = []

        for path_ending in ["athlete_events.csv", "athlete_events.csv"]:
            path = self._data_folder_path+stockname+path_ending
            stock = pd.read_csv(path, index_col = 0, parse_dates = True)
            stock.index.rename("Date", inplace=True)

            stock_df_list.append(stock)

        return stock_df_list

def tot_data():
    germany = df.tot_data()
    germany = germany[germany["NOC"] == "GER"].reset_index(drop=True)
        
    return germany
    