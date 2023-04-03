import requests
import json
import pandas as pd
import openpyxl


###### Retrieving JSON ######
def jira_get():
    authheader = {'Authorization' : 'Bearer JJrWJujcRL87s8wrRbml8iRBCw1eOKTylQHR8g'}
    json_data = []
    #search_response = requests.get(
    #    'https://reqcentral.com/rest/api/latest/search?jql=project=ndoc AND issuetype= "EDS Document" AND assignee= "Phillip Brade" OR assignee= "Jorge Bejarano" OR assignee= "Diana Chamorro" & maxResults=100',
    #     headers=authheader)
    #print(search_response.text)
    #json_txt = json.loads(search_response.text)
    #write_to_json('raw_dump.json',json_txt)
    #prep file
    try:
        #json_txt = json.loads(search_response.text)
        #write_to_json('raw_dump.json',json_txt)
        f = open('raw_dump.json')
        json_txt = json.load(f)
        #print(json_txt)
        #loop through and keep only the important info

        for keys in json_txt['issues']:
            entry = {}
            #search for summary and assignee
            successful = False
            
            try:
                entry['name'] = keys['key'] # json first level store NDOC name
                #assignee = str(keys['fields']['assignee']['name'])
                entry['rpats'] = str(keys['fields']['customfield_18675'])
                entry['summary'] = str(keys['fields']['subtasks'][0]['fields']['summary'])
                entry['assignee'] = str(keys['fields']['assignee']['name'])
                #summary = str(keys['fields']['subtasks'][0]['fields']['summary'])
                entry['status'] = str(keys['fields']['subtasks'][0]['fields']['status']['name'])
                #status = str(keys['fields']['subtasks'][0]['fields']['status']['name'])
                entry['created'] = str(keys['fields']['created'])
                updated = str(keys['fields']['updated'])
                description = str(keys['fields']['description'])
                info = []
                info.append({
                    #'assignee':assignee,
                    #'summary':summary,
                    'description' : description,
                    #'status' : status,
                    'updated' : updated
                    })
                entry['info'] = info
                successful = True

            # in case of missing info
            except:
                successful = False

            # appending info if info was captured
            if successful:    
                json_data.append(entry)
            
    # total failure  
    except:
        print('failed to update info')

    print(json_data)
    update = json_data
    file_to_update = 'dumpy.json'
    write_to_json(update, file_to_update)


# Helper Function to write to json
def write_to_json(data, filename):
    with open(filename,'w') as f:
        json.dump(data,f,indent=4)

# return json data
def serve_json_report():
    pd.read_json('dumpy.json').to_excel('output.xlsx')
################################################################
######### Do stuff area#########################################
jira_get()
serve_json_report()




#authheader = {'Authorization' : 'Bearer JJrWJujcRL87s8wrRbml8iRBCw1eOKTylQHR8g'}

#######TEST#########
#reponse = requests.get('https://reqcentral.com/rest/api/latest/search?jql=project=ndoc AND issuetype= "EDS Document" AND assignee= "Phillip Brade" OR assignee="Jorge Bejarano" & maxResults=100', headers=authheader)


#jsontxt = json.loads(reponse.text)
#f = open('eds_dump.json')
#jsontxt = json.load(f)

#try:
#    #print(jsontxt)
#    for keys in jsontxt['issues']:
#        #print(keys['key'])
#        try:
#            name = str(keys['fields']['assignee']['name'])
#            #print(name)
#            #print(keys['key'])
#            #print(keys['fields']['issuelinks'][0]['outwardIssue']['fields']['summary'])
#            #print(keys['fields']['assignee']['name'])
#            if name == 'Phillip.Brade@rci.rogers.com':
#                print(keys['key'])
#                print(keys['fields']['subtasks'][0]['fields']['summary'])
#                print(keys['fields']['assignee']['name'])
#        except:
#            name = ""
#
#except:
#    print(jsontxt)
#
#
#############################################################
