import os
import  readdat
from NCBIinfo_extract import Get_inform_NCBI
from Visualization_and_Save import result_df_to_veiw_pdf
# read file
file_path  = './Data/testdata.xlsx'
Sample_dat  = readdat.read_data(file_path=file_path)

# get info from SRA
email = "1666526339@qq.com"
Sample_dat = Get_inform_NCBI(Sample_dat=Sample_dat,email=email)

# save result
save_path = "./Result"
save_path = os.path.join(save_path,"result.pdf")
print(save_path)
wkhtmltopdf_path = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
result_df_to_veiw_pdf(Data=Sample_dat,save_path=save_path,wkhtmltopdf_path=wkhtmltopdf_path)







