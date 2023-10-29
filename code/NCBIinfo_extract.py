from Bio import Entrez
import readdat
import  pandas as pd
import GEOparse
import xmltodict
import json
from pandas import DataFrame, read_excel

# GSM 信息获取
def get_info_from_GSM(GSM: str) ->dict:
    """_summary_
    基于GSMID获取GEO中的信息,包括Biosample信息。
    Args:
        GSM (_type_): GSMID如GSM123456

    Returns:
        _type_: dict 包含GEO中的信息
    """
    gse = GEOparse.get_GEO(geo=GSM,destdir="../Data/TMP/",geotype="GSM")
    gsemetadata = gse.metadata
    return gsemetadata
# SRA数据数据库信息获取 DRX, ERX, SRX
def Get_info_from_SRA(ID: str,email: str)-> dict:
    """解析Biopython SRA数据库返回的XML结果获取ERX, SRX, DRX的信息在SRA中的信息
    
    Args:
        ID (str): _description_
        email (str): _description_

    Returns:
        dict: _description_
    """ 
    Entrez.email = email
    Entrez.tool = "MyLocalScript Use to get the experitment information of SRA"
    id = ID
    print(id)
    # 基于ID获取SRA的信息，转化为字典
    sra_id_list = Entrez.read(Entrez.esearch(db="sra",term=id))["IdList"]
    if sra_id_list.__len__() == 1:
        sra_id = sra_id_list[0]
    else:
        print("sra_id_list is not noly one ,the {id} will be skip".format(id=id))
        return {}
    
    sra_record =Entrez.efetch(db="sra",id=sra_id,retmode ='xml',rettype = "xml" ).read()
    sra_record_dict = xmltodict.parse(sra_record.decode("utf-8"))
    sra_content = sra_record_dict["EXPERIMENT_PACKAGE_SET"]["EXPERIMENT_PACKAGE"]
    new_sra_content = {}
    
    
    if len(set(sra_record_dict.keys())-set(['EXPERIMENT', 'SUBMISSION', 'Organization', 'STUDY', 'SAMPLE', 'Pool', 'RUN_SET']))>0:
        print("*"*20)
        print(set(sra_record_dict.keys())-set(['EXPERIMENT', 'SUBMISSION', 'Organization', 'STUDY', 'SAMPLE', 'Pool', 'RUN_SET']))
        print("*"*20)
        if len(set(sra_record_dict.keys())-set(['EXPERIMENT', 'SUBMISSION', 'Organization', 'STUDY', 'SAMPLE', 'Pool', 'RUN_SET']))==1 and "EXPERIMENT_PACKAGE_SET" in set(sra_record_dict.keys()):
            sra_record_dict = sra_record_dict["EXPERIMENT_PACKAGE_SET"]["EXPERIMENT_PACKAGE"]        
        
    # 信息收集
    # ['EXPERIMENT', 'SUBMISSION', 'Organization', 'STUDY', 'SAMPLE', 'Pool', 'RUN_SET'] 现在处理这些标签，后续测试再查看是否需要其他标签
    new_sra_content["TITLE"] = sra_content["EXPERIMENT"]["TITLE"]
    new_sra_content["SRA_ID"] = sra_content["EXPERIMENT"]["@accession"]
    new_sra_content["STUDY_REF"] = sra_content["EXPERIMENT"]["STUDY_REF"]["@accession"]
    new_sra_content["BioProject"] = sra_content["STUDY"]["IDENTIFIERS"]["EXTERNAL_ID"]["#text"] #防止有多个ID需要验证下
    new_sra_content["DESIGN"] ={}
    new_sra_content["DESIGN"]["DESIGN_DESCRIPTION"] = sra_content["EXPERIMENT"]["DESIGN"]["DESIGN_DESCRIPTION"]
    new_sra_content["DESIGN"]["SAMPLE_DESCRIPTOR"] = sra_content["EXPERIMENT"]["DESIGN"]["SAMPLE_DESCRIPTOR"]       # 后面实验下看要不要删除感觉内容多余
    new_sra_content["LIBRARY_DESCRIPTOR"] = sra_content["EXPERIMENT"]["DESIGN"]["LIBRARY_DESCRIPTOR"] #
    new_sra_content["PLATFORM"] = sra_content["EXPERIMENT"]["PLATFORM"] # 测序平台 后面看看存不存在不兼容或者没有这部分数据的问题
    new_sra_content["SUBMISSION_lab_name"] = sra_content["SUBMISSION"]["@lab_name"]
    new_sra_content["DESCRIPTOR"]  = {}
    new_sra_content["DESCRIPTOR"]  = sra_content["STUDY"]["DESCRIPTOR"] # 可能在有的键和值存在重复考虑去重
    new_sra_content["Biosample_ID"] = sra_content["Pool"]["Member"]["IDENTIFIERS"]["EXTERNAL_ID"]["#text"] # 判断下这个EXTERNAL_ID字典下@namespace是否为BioSample
    return new_sra_content


def Get_inform_NCBI(Sample_dat:DataFrame,email: str = '1666526339@qq.com')->DataFrame:
    Sample_dat["type"] = Sample_dat["Sample"].str[:3]
    # 默认使用Sample列，如果没有就要用户修改一列Sample
    Sample_type_dict = dict(tuple(Sample_dat.groupby("type").Sample))

    if len(list(set(Sample_type_dict.keys() )-set(['DRX', 'ERX', 'GSM', 'SRX']) ) ) == 0 :
        print("Sample type is right")
    else:
        error_type = list(set(Sample_type_dict.keys() )-set(['DRX', 'ERX', 'GSM', 'SRX']) ) 
        print( f"""Sample type is wrong, please check the type of {",".join(error_type)} ,it should be DRX, ERX, GSM or SRX.""")

    # 判断数据来源
    Sample_dat["database"] = Sample_dat["type"].map(lambda x: "GEO" if x == "GSM" else "SRA")
    Sample_dat["info"] = Sample_dat.apply(lambda x: get_info_from_GSM(x["Sample"]) if x["database"]=="GEO" else Get_info_from_SRA(x["Sample"],email) ,axis=1)
    Sample_dat["info"] = Sample_dat["info"].map(lambda x: x if isinstance(x,dict) else {})
    Sample_dat['info'] = Sample_dat["info"].map(lambda x : json.dumps(x,ensure_ascii=False) if x!={} else x)
    return Sample_dat

if __name__ == "__main__":
    email = "1666526339@qq.com"
    file_path = "./Data/testdata.xlsx"

    file_path  = file_path
    Sample_dat  = readdat.read_data(file_path=file_path)
    Sample_dat["type"] = Sample_dat["Sample"].str[:3]
    # 默认使用Sample列，如果没有就要用户修改一列Sample
    Sample_type_dict = dict(tuple(Sample_dat.groupby("type").Sample))

    if len(list(set(Sample_type_dict.keys() )-set(['DRX', 'ERX', 'GSM', 'SRX']) ) ) == 0 :
        print("Sample type is right")
    else:
        error_type = list(set(Sample_type_dict.keys() )-set(['DRX', 'ERX', 'GSM', 'SRX']) ) 
        print( f"""Sample type is wrong, please check the type of {",".join(error_type)} ,it should be DRX, ERX, GSM or SRX.""")

    # 判断数据来源
    Sample_dat["database"] = Sample_dat["type"].map(lambda x: "GEO" if x == "GSM" else "SRA")
    Sample_dat["info"] = Sample_dat.apply(lambda x: get_info_from_GSM(x["Sample"]) if x["database"]=="GEO" else Get_info_from_SRA(x["Sample"],email) ,axis=1)
    Sample_dat["info"] = Sample_dat["info"].map(lambda x: x if isinstance(x,dict) else {})
    Sample_dat['info'] = Sample_dat["info"].map(lambda x : json.dumps(x,ensure_ascii=False) if x!={} else x)
    Sample_dat.to_excel("./Result/testdata.xlsx",index=False)
    print(Sample_dat.head())






# 关键信息获取,Biosample ,ERP, SRA
# 实际上DRX, ERX, SRX都是SRA的ID，代表的不同数据库ENA, DDBJ, NCBI.而GSM是GEO的ID。










