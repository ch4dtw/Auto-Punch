#-*- coding: UTF-8 -*-
import requests
import re
from config import account,password,projectID,hour
from BeautifulSoup import BeautifulSoup as bs4

s = requests.session()
# initial request paraments
urlLogin = "https://signin.fcu.edu.tw/clockin/login.aspx"
header = {
  'Host':'signin.fcu.edu.tw',
  'Content-Type':'application/x-www-form-urlencoded',
  'Referer':'https://signin.fcu.edu.tw/clockin/login.aspx',
  'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'
}
# get initial page session
r = s.get(urlLogin)
response = bs4(r.text)
# initial login paraments
postdataLogin = {
  'i__EVENTTARGET':'',
  '__EVENTARGUMENT':'',
  'LoginLdap$LoginButton':'登入'
}

# parse form data
for element in response.findAll('input',{'type':'hidden','value':True}):
  postdataLogin[str(element['name'])] = str(element['value'])
postdataLogin['LoginLdap$UserName'] = account
postdataLogin['LoginLdap$Password'] = password
# log in
loginHtml = s.post(urlLogin,data=postdataLogin,headers=header)
response = bs4(loginHtml.text)
# initial sign in paraments
urlSign = "https://signin.fcu.edu.tw/clockin/Student.aspx"
postdataSign = {
  'ButtonAssistantClockin':'計畫助理簽到'
}

# parse form data
for element in response.findAll('input',{'type':'hidden','value':True}):
  postdataSign[str(element['name'])] = str(element['value'])
# log in
signInHtml = s.post(urlSign,data=postdataSign,headers=header)
response = bs4(signInHtml.text)
# initial sign in paraments
urlCheck = "https://signin.fcu.edu.tw/clockin/AssistantClockin.aspx"
postdataCheck = {
  'DropDownListProject': projectID,
  'DropDownListHour': hour,
  'ButtonClockin':'簽到'
}

# parse form data
for element in response.findAll('input',{'type':'hidden','value':True}):
  postdataCheck[str(element['name'])] = str(element['value'])
# log in
checkHtml = s.post(urlCheck,data=postdataCheck,headers=header)
response = bs4(checkHtml.text)
print account + ', ' + projectID + ', ' + str(hour) + 'hr, ' + re.findall('alert\(\'(.*)\'\)',response.text)[0]
