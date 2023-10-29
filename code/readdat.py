import pandas as pd
from typing import  Union
def read_data(file_path: str, sheetname: Union[int, str] = 1) -> pd.DataFrame:
    """Read data from a file.

    Args:
        file_path (str): Path to the file.
        sheetname (Union[int, str]): Name or index of the sheet to read from. Default is 1.

    Returns:
        pd.DataFrame: Data in DataFrame format.
    """
    file_extension = file_path.split('.')[-1]
    if file_extension == 'csv':
        return pd.read_csv(file_path)
    elif file_extension == 'txt':
        return pd.read_csv(file_path, sep='\t')
    elif file_extension == 'xlsx' :
        return pd.read_excel(file_path,)
    elif file_extension == "xls" :
        return pd.read_excel(file_path,engine='xlrd')
    else:
        raise ValueError(f'Unsupported file format: {file_extension},please USE  txt,excel,xlsx,xls ')



if __name__ == '__main__':
    # file_path = input('Enter the path to your data file: ')
    file_path = "../lib_base_info_more1M_reads.xls"
    data = read_data(file_path,sheetname="lib_base_info_more1M_reads")
    print(data.head())  # Print the first 5 rows of the data