
# coding: utf-8

# In[2]:


import pandas as pd
input_df = pd.read_csv('D:\\python_examples\\code\\classif\\02-09-2018\\PII_Tag -students\\000000_0','\001')
#arc_data.columns()
input_df.columns
#print(input_df.head(3))
#input_data_columns=['email','country_code_iso2','first_name','last_name','phone','ip']
input_data_columns=['email','phone','ip']
output_field = ['field_length','is_numeric','domain_sep_count','has_dot_aft_at','dot_count',
                'is_ip_pattern','is_double','hyphen_count','has_plus','label']
#print('input_data_columns-> ',input_data_columns)
#print('output_field-> ',output_field)

input_addr_df2 = pd.read_csv('D:\\python_examples\\code\\classif\\02-09-2018\\PII_Tag -students\\ip_addr')
input_phone_df3 = pd.read_csv('D:\\python_examples\\code\\classif\\02-09-2018\\PII_Tag -students\\phone_num')
final_data = pd.concat([input_df, input_phone_df3,input_addr_df2], axis=1)
print(final_data.head())
#print(input_df.head())
#OUTPUT
#Label field_length, is_numeric, domain_sep_count, has_dot_aft_at, dot_count, 
#is_IP_pattern, is_double ,hyphen_count ,has_plus


# In[3]:


import re
feature_dict=dict()
def get_field_length(data):
    try :
        return len(data)
    except:
        return 0

def is_numeric(data):
    try :
        if(data.isdigit()):
            return 1
        else:
            return 0
    except:
        return 0

def domain_sep_count(data):
    try:
        return data.count('@')
    except:
        return 0
    
def has_dot_aft_at(data):
    try:
        if(data.index('@') > 0):
            subset_aft_at=data[data.index('@')+1:]
            if dot_count(subset_aft_at) > 0 :
                return 1
            else :
                return 0        
    except:
        return 0
    
def dot_count(data):
    try:
        return data.count('.')
    except:
        return 0
    
def is_ip_pattern(data):
    ippattern = '([1-2]?[0-9]?[0-9]\.){1,3}([1-2]?[0-9]?[0-9])?'
    try:
        return  1 if re.match(ippattern, data) else 0
    except:
        return 0
    
def is_double(data):
    try:
        return 1 if type(data) == float else 0
    except:
        return 0

def hyphen_count(data):
    try:
        return data.count('-')
    except:
        return 0
    
def has_plus(data):
    try:
        return 1 if data[0]=='+' else 0
    except:
        return 0
    
def generate_feature_list(colName
                          ,data
                          ,get_field_length
                          ,is_numeric
                          ,domain_sep_count
                          ,has_dot_aft_at
                          ,dot_count
                          ,is_ip_pattern
                          ,is_double
                          ,hyphen_count
                          ,has_plus):
      return (get_field_length(data)
            ,is_numeric(data)
            ,domain_sep_count(data)
            ,has_dot_aft_at(data)
            ,dot_count(data)
            ,is_ip_pattern(data)
           ,is_double(data)
           ,hyphen_count(data)
           ,has_plus(data)
           ,colName)
        
#print(has_dot_aft_at("111.1"))
#print(email)


# In[5]:


file_object  = open("D:\\python_examples\\code\\classif\\02-09-2018\\PII_Tag -students\\pii_feature_current.csv", "w")
total_row_list=list()
for eachColName in input_data_columns :
    feature_data = final_data[eachColName]
    for colData in feature_data.head(100000) :
        eachRow=generate_feature_list(eachColName
                              ,colData
                              ,get_field_length
                             ,is_numeric
                             ,domain_sep_count
                             ,has_dot_aft_at
                             ,dot_count
                             ,is_ip_pattern
                             ,is_double
                             ,hyphen_count
                             ,has_plus)
        total_row_list.append(eachRow)

file_object.write(','.join(str(colVal) for colVal in output_field) + '\n')
for item in total_row_list:
    file_object.write(','.join(str(colVal) for colVal in item) + '\n')
file_object.close()

