import requests
from config import account, password
wifi_login='http://140.134.18.25/auth/index.html/u'
wifi_data={
'user':account,
'password':password,
'PtButton':'Logon'
}
r=requests.post(wifi_login,data=wifi_data)
print r.text
