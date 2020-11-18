import requests    
from datetime import datetime
import pandas as pd

column_names = ["Link", "Is_Link_Active", "Is_Link_Not_Active", "Link_HTTP_status", "Date"]

df = pd.DataFrame(columns = column_names)

my_input_file = pd.read_csv("urls.csv")
#Select the column with the links to be checked and save it as a list.
page_list = my_input_file['wpcf-website']

for page in page_list:
	try:	
		http_status = str(requests.get(page, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10))
		print ('URL: ', page,'Status: ', http_status)    
		if http_status == '<Response [200]>':
			df = df.append(pd.Series([page, True, False, http_status, datetime.today().strftime('%Y-%m-%d-%H:%M:%S')], index=df.columns ), ignore_index=True)
		else:
			df = df.append(pd.Series([page, False, True, http_status, datetime.today().strftime('%Y-%m-%d-%H:%M:%S')], index=df.columns ), ignore_index=True)
	except (requests.ConnectionError, requests.ReadTimeout, requests.Timeout) as e:
		print("An exception occurred:", e, " --- ", http_status)
		pass 
print(df)
df.to_csv ('export_dataframe.csv', index = False, header=True)

# To improve add the SSL Certificate maybe? 
