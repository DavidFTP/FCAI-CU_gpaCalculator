# fill out those fields then run teh code
USERNAME = '<your student ID>' # 20200000
PASSWORD = '<your password>' # password
termEnder = 'Fundamentals of Economies' # to stop calculating at a specific subject
calculateFails = False

import requests
import json
from prettytable import PrettyTable

# Step 1: Authenticate
login_url = 'http://newecom.fci-cu.edu.eg/api/authenticate'
headers = {'Content-Type': 'application/json'}
payload = {
  'username': USERNAME,
  'password': PASSWORD, 
  'rememberMe': True
}
response = requests.post(login_url, json=payload, headers=headers)
if response.status_code == 200:
    access_token = response.json()['id_token']
    print('Successfully authenticated!')
else:
    print('Authentication failed:', response.json()['message'])

# Step 2: Use the access token
grade_url = f'http://newecom.fci-cu.edu.eg/api/student-courses?size=150&studentId.equals={USERNAME}&includeWithdraw.equals=true'
headers = {'Authorization': 'Bearer ' + access_token}
response = requests.get(grade_url, headers=headers)
if response.status_code == 200:
  data = json.loads(response.content)
else:
  print('Error:', response.status_code)

# step 3: Display in a table 
table = PrettyTable()
table.field_names = ['name', 'grade', 'hours', 'multiple']
for course in data:
  #! this condition you can manually fill if you want to stop at a specific term
  # if (course['course']['name'] == termEnder):
  #   break
  if (calculateFails):
    table.add_row([course['course']['name'], course['grade'], course['course']['numOfHours'], course['points']])
  else:
    if course['grade'] != 'F':
      table.add_row([course['course']['name'], course['grade'], course['course']['numOfHours'], course['points']])
print(table)

# step 4: Calculate GPA
# iter(grade * point) + all
# divide by sum of all credit hours by
earnt = 0
total = 0
for course in data:
  #! this condition you can manually fill if you want to stop at a specific term
  # if (course['course']['name'] == termEnder):
  #   break
  if (calculateFails):
    earnt += course['points'] * course['course']['numOfHours']
    total += course['course']['numOfHours'] * 4
  else:
    if (course['grade'] != 'F'):
      earnt += course['points'] * course['course']['numOfHours']
      total += course['course']['numOfHours'] * 4

GPA = earnt * 4 / total
out = '{:.3f}'.format(GPA)
print(f'Your GPA is ==>  \033[30;47m{out}\033[m  <==')