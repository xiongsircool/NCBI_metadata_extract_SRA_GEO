import pandas as pd
from pandas import DataFrame, read_excel
import pdfkit
import json

# 基于字典进行可视化
def format_json_to_html(data, indent=0):
    html_content = ''
    indent_str = '  ' * indent
    if isinstance(data, dict):
        for key, value in data.items():
            if value is None or value == '' or len(value) == 0:
                continue  # Skip keys with None or empty string values
            if isinstance(value, (dict, list)):
                html_content += f'{indent_str}<strong>{key}:</strong><br>'
                html_content += format_json_to_html(value, indent + 1)
            else:
                if isinstance(value, str):
                    # Handle special characters
                    value = value.replace('掳', '°').replace('飩癈', '°C').replace('渭mol', 'μmol').replace('m鈭2 s鈭1', 'm−2 s−1').replace('掳', '&deg;').replace('碌', '&micro;').replace('m−2', 'm<sup>-2</sup>').replace('s−1', 's<sup>-1</sup>').replace('°', '&deg;').replace('μ', '&micro;').replace('鈥揼', '--')

                html_content += f'{indent_str}<strong>{key}:</strong> {value}<br>'
    elif isinstance(data, list):
        for item in data:
            # Handle special characters for list items
            if isinstance(item, str):
                item = item.replace('掳', '°').replace('飩癈', '°C').replace('渭mol', 'μmol').replace('m鈭2 s鈭1', 'm−2 s−1').replace('掳', '&deg;').replace('碌', '&micro;').replace('m−2', 'm<sup>-2</sup>').replace('s−1', 's<sup>-1</sup>').replace('°', '&deg;').replace('μ', '&micro;').replace('鈥揼', '--')
            html_content += f'{indent_str}{item}<br>'
    return html_content
# 

def result_df_to_veiw_pdf(Data:DataFrame,save_path:str,wkhtmltopdf_path:str = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'):
    """
    1 将DataFrame数据转换为PDF文件,按照Sample列进行分组
    2 
    Args:
        Data (DataFrame): 上一步处理的结果
        save_path (str):  设置保存文件的路径
        wkhtmltopdf_path (str): wkhtmltopdf.exe的路径,默认为C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe
    """
    df = Data
    df = df.sort_values("type")
    # Convert the table data to HTML format
    html_content = '<h1>Table Data to PDF</h1>'
    
    html_content_all = '' 

    for index, row in df.iterrows():
        html_content_single = f'<h2>{row["Sample"]}</h2>'
        
        table_dat = row[~row.index.isin(["Sample","info"])]
        html_content_single_table = '<table >'
        for i in range(len(table_dat)):
            html_content_single_table += f'<tr><td>{table_dat.index[i]}</td><td>{table_dat[i]}</td></tr>'
        html_content_single_table += '</table>'
        html_content_single += html_content_single_table
        html_content_single += '<h3>Info</h3>'    
        info_data = json.loads(row['info'])
        html_content_single += format_json_to_html(info_data)
        html_content_all += html_content_single
        html_content_all += '<br>'
        html_content_all += '<hr>'  
        
    html_content += html_content_all     
    # Convert the HTML content to PDF using pdfkit
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdfkit.from_string(html_content,save_path, configuration=config)


from pandas import DataFrame, read_excel

if __name__ == "__main__":
    # Read data from testdata.xlsx file
    sample_data = read_excel('Result/testdata.xlsx')

    # Generate PDF file using result_df_to_veiw_pdf function
    result_df_to_veiw_pdf(sample_data, 'Result')
