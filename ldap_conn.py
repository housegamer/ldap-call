import ldap3
import time
import csv, json, os, ssl, sys
import getpass
import logging
from ldap3.utils.log import set_library_log_detail_level, get_detail_level_name, set_library_log_hide_sensitive_data, BASIC, NETWORK, EXTENDED, PROTOCOL, ERROR
from ldap3 import Server, Connection, ALL, Tls, NTLM, SUBTREE


username = input('Please put expedia username: ')
password = getpass.getpass('Please put prod password: ')

def logs():
    timestr = time.strftime('%m-%d-%Y:%H-%M-%S')
    path = f'/Users/rodcastillo/Documents/LdapLogs/log-{timestr}.log' # Use your personal/server path
    set_library_log_detail_level(BASIC)
    return path

def conn():
    tls_configuration = Tls(validate=ssl.CERT_REQUIRED,version=ssl.PROTOCOL_TLSv1)
    logging.basicConfig(filename=f'{logs()}', level=logging.DEBUG)
    server = Server("ldaps://lbdc.sea.corp.expecn.com:636", use_ssl=True, get_info=ldap3.ALL) # Use your own LDAP connections
    conn = Connection(server,
                     user=f'expediagroup.com\\{username}',  
                     password=f'{password}', 
                     authentication=NTLM,
                     auto_bind=True,
                     check_names=True,
                     return_empty_attributes=False,
                     client_strategy=ldap3.SYNC,
                     auto_referrals=True,
                     use_referral_cache=True)
    conn.start_tls()
    conn.extend.standard.paged_search("DC=sea,DC=corp,dc=expecn,dc=com", 
                                        "(&(givenName=*))",
                                        attributes=['givenName','sn','mail','manager','sAMAccountName','proxyAddresses'],#primaryGroupID
                                        paged_size=2000, 
                                        size_limit=0,
                                        generator=False,
                                        search_scope=ldap3.SUBTREE)
    entry = conn.entries
#entry = conn.entries[4].entry_to_json()
#print("The total of entrys is: ", len(entry))
    return entry
print(conn())
print('Done')

def main():
    pass

#def file_comparation():

# Read ldap file and qubole file
# ldapFile = pd.read_excel('/Users/rodcastillo/Documents/TestLDAP/test10_expediagroup_domain.xlsx')
# quboleFile = pd.read_excel('/Users/rodcastillo/Documents/TestLDAP/quboleFullResult.xlsx')
# #print(ldapFile.columns)
# #print(quboleFile.columns)

# # Turn the column into a list
# ldap_file_ref = ldapFile['Name'].tolist()
# ldap_file_ref1 = ldapFile['Email'].tolist()

# qubole_file_ref = quboleFile['account_name'].tolist()
# qubole_file_ref1 = quboleFile['email'].tolist()

# # Turn the columns from a list to a dictonary 
# ldap_file_dict = dict(zip(ldap_file_ref,ldap_file_ref1))
# qubole_file_dict = dict(zip(qubole_file_ref,qubole_file_ref1))

# # Create file variable to ouput data
# filename = '/Users/rodcastillo/Documents/TestLDAP/outputFileTest1.csv'
# f = open(filename, 'w')

# headers = 'Name, Email, Account_name, Dup_email'
# f.write(headers)

# # Loop through ldap file and qubole file dictionary and search for match emails
# for Name, Email in ldap_file_dict.items():
#     for account_name, email in qubole_file_dict.items():
#         x = re.search(Email,email)
#         if x:
#             match = x.group()
#             pos = x.start() + 1
#             f.write(str(Name) + ',' + Email + ',' + account_name + ',' + email + ',' + match + '\n')
# f.close()
#file_comparation()

# if __name__ == "__main__":
#     conn() 

