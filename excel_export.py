import pandas as pd 
import xlsxwriter
import ldap_conn
import time


# Creating date and time for ordering purpose
timestr = time.strftime('%m-%d-%Y:%H-%M')

# Writing out to a excel sheet - uncomment and put your own path to writeout excel
df = pd.DataFrame(ldap_conn.conn())
writer = pd.ExcelWriter(f'/Users/rodcastillo/Documents/TestLDAP/test_export_{timestr}.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Test', index=True) # header=['givenName','sn','mail','manager','sAMAccountName','proxyAddresses'] 
writer.save()

print("Done")
