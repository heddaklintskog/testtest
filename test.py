from urllib.parse import urlencode

from datetime import date, datetime, timedelta
import time
import requests



x=datetime.now()
date_N_days_ago = x - timedelta(days=2000)

delete_date=date_N_days_ago.strftime("%Y-%m-%d")
print(delete_date)


print('################')


user = 'hedda.klintskog@storytel.com'+'/token'



params = {
 
    'query': 'type:ticket status:closed solved<'+delete_date,
    'sort_by': 'created_at', 
    'sort_order': 'asc'
}


url = 'https://storytelsupport.zendesk.com/api/v2/search.json?' + urlencode(params)
response =  requests.get(url, auth=(user, pwd))   #session.get(url)
if response.status_code != 200:
    print('Status:', response.status_code, 'Problem with the search request. No tickets will be deleted. Exiting')
    exit()

# Print the subject of each ticket in the results
data = response.json()

big_array=[]
id_list=[]

for result in data['results']:
    arr=[result['id'],  result['updated_at'], result['subject']]
    id_list.append(arr)
big_array.append(id_list)
print(len(id_list))
if(len(id_list)==0): #If there's no tickets, exit.
    print('No tickets to delete. Exiting')
    exit()
    

next=data["next_page"]
count=data['count']


while(next != None): #Loop while there's new tickets to fetch
    
    print('*')
    time.sleep(1) #Delay to prevent "429 Too Many Requests" 
    url=data["next_page"]
    response =  requests.get(url, auth=(user, pwd))   
    if response.status_code != 200: #if the request wasn't successfull 
        print('Status:', response.status_code, 'Problem with search the request. All tickets might not be deleted.')
        next= None
    else:
 
        # Print the subject of each ticket in the results
        data = response.json()
       
        id_list=[]
        for result in data['results']:
            
            arr=[result['id'],  result['updated_at'], result['subject']]
            
            id_list.append(arr)
        
            

        big_array.append(id_list)
        next=data["next_page"]

i=0
#Delete tickets, 100 at a time
for ids in big_array:
    delt='ids='+ ','.join(str(e[0]) for e in ids)

    if( len(ids) == 0):
        print('Something went wrong. All ticket might not been deleted')
        
    else:
        time.sleep(1) #Delay to prevent "429 Too Many Requests" 
        url='https://storytelsupport.zendesk.com/api/v2/tickets/destroy_many.json?'+delt
        response= requests.delete(url, auth=(user, pwd))  
        if response.status_code != 200:
            print('-------------------Status:', response.status_code, 'Problem with the delete request.------------------------------------')
            print(delt)
        else:
            
            for arr in ids:
                i=i+1
                print(arr[0], ' ', arr[1])

    
print(i, 'of', count) 
