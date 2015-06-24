####Functions####
def state_replace(s):
    state = {'01':'Alabama','02':'Alaska','04':'Arizona','05':'Arkansas',\
            '06':'California','08':'Colorado','09':'Connecticut',\
            '10':'Delaware','11':'DC','12':'Florida','13':'Georgia',\
            '15':'Hawaii','16':'Idaho','17':'Illinois','18':'Indiana',\
            '19':'Iowa','20':'Kansas','21':'Kentucky','22':'Louisiana',\
            '23':'Maine','24':'Maryland','25':'Massachusetts','26':'Michigan',\
            '27':'Minnesota','28':'Mississippi','29':'Missouri',\
            '30':'Montana','31':'Nebraska','32':'Nevada','33':'New Hampshire',\
            '34':'New Jersey','35':'New Mexico','36':'New York',\
            '37':'North Carolina','38':'North Dakota','39':'Ihio',\
            '40':'Oklahoma','41':'Oregon','42':'Pennsylvania',\
            '44':'Rhode Island','45':'South Carolina','46':'South Dakota',\
            '47':'Tennessee','48':'Texas','49':'Utah','50':'Vermont',\
            '51':'Virginia','53':'Washington','54':'West Virginia',\
            '55':'Wisconsin','56':'Wyoming','72':'Puerto Rico'}
    return state[s]
    
def int_convert(s):
    try:
        l = int(s)
    except ValueError:
        l = s
    return l

####Python Libraries####
import ast
import urllib2
import pandas as pd

####Constants####

#The census year
year = 2010
#The census dataset
dataset = 'sf1'
#The API key to access the census data (unique to user)
with open('key.txt','r') as k:
    key = k.read()
#These are the reference numbers for each state (and territory)
state_num = ['01','02','04','05','06','08','09','10','11','12','13','15','16',\
            '17','18','19','20','21','22','23','24','25','26','27','28','29',\
            '30','31','32','33','34','35','36','37','38','39','40','41','42',\
            '44','45','46','47','48','49','50','51','53','54','55','56','72']
#Initialize the population dataset
pop_data = pd.DataFrame()

####Existing Dataset (~100,000 rows)####

#Read in the existing dataset. Assume (for now) that current data is clean enough
#existing_data = pd.read_json('existing_dataset.json')

####Population Data####

    #Create the base API url for accessing the census data
base_api_url = 'http://api.census.gov/data/%s/%s?key=%s&get=' % (str(year), dataset, key)

for s in state_num:
        #Read in total population, population by race, and housing 
    pop_url = base_api_url + 'P0010001,P0060002,P0060003,P0060004,P0060005,P0060006,P0060007,H0030001,H0030003&for=zip+code+tabulation+area:*&in=state:%s' % s
        #Send a request for the data and read it out
    req = urllib2.Request(pop_url)
    response = urllib2.urlopen(req)
    temp = response.read()
        #Evaluate the response into a list of values roken down by zip code
        #for a single state
    state_data = ast.literal_eval(temp.decode('utf8'))
        #Add the current state's data to the total population data
    pop_data = pd.concat([pop_data,pd.DataFrame(state_data[1:])],ignore_index = True)

    #Create column headers for ease of identification
pop_data.columns = ['Total_Population',\
                    'White_Population',\
                    'Black_Population',\
                    'American_Indian_Alaska_Native_Population',\
                    'Asian_Population',\
                    'Native_Hawaiian_Pac_Islander_Population',\
                    'Other_Race_Population',\
                    'Occupied_Housing',\
                    'Vacant_Housing',\
                    'State_Code',\
                    'Zip_Code'] 

####Dataset Prep####
#This section will convert all data into the proper formats and make them as 
#usable as possible
    #Replace the state code with actual state names
pop_data['State_Code'] = pop_data['State_Code'].map(lambda x: state_replace(x))
    #Convert all numeric strings (except zip code) to integers
pop_data['Total_Population'] = pop_data['Total_Population'].map(lambda x: int_convert(x))
pop_data['White_Population'] = pop_data['White_Population'].map(lambda x: int_convert(x))
pop_data['Black_Population'] = pop_data['Black_Population'].map(lambda x: int_convert(x))
pop_data['American_Indian_Alaska_Native_Population'] = pop_data['American_Indian_Alaska_Native_Population'].map(lambda x: int_convert(x))
pop_data['Asian_Population'] = pop_data['Asian_Population'].map(lambda x: int_convert(x))
pop_data['Native_Hawaiian_Pac_Islander_Population'] = pop_data['Native_Hawaiian_Pac_Islander_Population'].map(lambda x: int_convert(x))
pop_data['Other_Race_Population'] = pop_data['Other_Race_Population'].map(lambda x: int_convert(x))
pop_data['Occupied_Housing'] = pop_data['Occupied_Housing'].map(lambda x: int_convert(x))
pop_data['Vacant_Housing'] = pop_data['Vacant_Housing'].map(lambda x: int_convert(x))




