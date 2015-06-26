####Functions####

    #This replaces the numerical state (FIPS) number with an actual state name
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
    
    #This converts a value to an integer (if possible).
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
    #Initialize the income dataset
inc_data = []

####Existing Dataset (~100,000 rows)####
#This section reads in a fictional dataset based on the parameters given in the 
#assignment. There is just a numerical assignment and random assortment of zip 
#codes.

    #Read in the (fictional) existing dataset. Assume (for now) that current 
    #data is clean enough
existing_data = pd.read_csv('existing_dataset.csv')
    #Make sure the zip code data is in string form for proper comparison to 
    #the rest of the zip code data.
existing_data['Zip_Code'] = existing_data['Zip_Code'].map(lambda x: str(x))

####Population Data####
#This section pulls population data as a function of zip code by state. Due to
#the way the database is set up, I had to designate a state to look at. This
#means that I have to loop through each state. 

    #The census year
year = 2010
    #The census dataset
dataset = 'sf1'
    #Create the base API url for accessing the census data
base_api_url = 'http://api.census.gov/data/%s/%s?key=%s&get='\
                 % (str(year), dataset, key)

for s in state_num:
        #Read in total population and population by race
    pop_url = base_api_url + '%s&for=zip+code+tabulation+area:*&in=state:%s'\
        % ('P0010001,P0060002,P0060003,P0060004,P0060005,P0060006,P0060007',s)
        #Send a request for the data and read it out
    req = urllib2.Request(pop_url)
    response = urllib2.urlopen(req)
    temp = response.read()
        #Evaluate the response into a list of values broken down by zip code
        #for a single state
    state_pop_data = ast.literal_eval(temp.decode('utf8'))
        #Add the current state's data to the total population data
    pop_data = pd.concat([pop_data,pd.DataFrame(state_pop_data[1:])],\
                            ignore_index = True)

    #Create column headers for ease of identification
pop_data.columns = ['Total_Population',\
                    'White_Population',\
                    'Black_Population',\
                    'American_Indian_Alaska_Native_Population',\
                    'Asian_Population',\
                    'Native_Hawaiian_Pac_Islander_Population',\
                    'Other_Race_Population',\
                    'State_Code',\
                    'Zip_Code'] 

####Median Income Data####
#This section pulls in the median income data from the ACS 5 year survey in 
#2015. As some of the median income is missing for some zip codes (shows as
# null), the output could not be literally evaluated using ast.literal_eval().
#The formatting had to be taken care of manually.  

    #The census year
year = 2013
    #the census dataset
dataset = 'acs5'
    #Create the base API url for accessing the census data
base_api_url = 'http://api.census.gov/data/%s/%s?&get=' % (str(year), dataset)

#for s in state_num:
    #Read in the median income by zip code 
inc_url = base_api_url + '%s&for=zip+code+tabulation+area:*&key=%s' \
        % ('B19326_001E',key)
    #Send a request for the data and read it out
req = urllib2.Request(inc_url)
response = urllib2.urlopen(req)
temp = response.read()
    #As this data can't just be literally evaluated (due to 'null'), we need to
    #do it manually. First, remove the erroneous characters and turn the single
    #large string into a list.
temp_data = temp.replace('[','').replace(']','').replace('"','').split()
    #Loop through all the intems in the list and split them into their two 
    #categories. The last comma will be taken care of later in the clean up 
    #phase.
for row in temp_data:
    inc_data.append(row.split(',',1))
    #Turn the list into a dataframe (We don't need the first 4 rows)
inc_data = pd.DataFrame(inc_data[4:])
    #Create column headers for ease of identification
inc_data.columns = ['Median_Income',\
                    'Zip_Code'] 

####Dataset Prep####
#This section will convert the data to more usable forms

    #Replace the state code with actual state names
pop_data['State_Code'] = pop_data['State_Code'].map(lambda x: state_replace(x))
#    #Convert all numeric strings (except zip code) to integers
#pop_data['Total_Population'] = pop_data['Total_Population']\
#                        .map(lambda x: int_convert(x))
#pop_data['White_Population'] = pop_data['White_Population']\
#                        .map(lambda x: int_convert(x))
#pop_data['Black_Population'] = pop_data['Black_Population']\
#                        .map(lambda x: int_convert(x))
#pop_data['American_Indian_Alaska_Native_Population'] = \
#                        pop_data['American_Indian_Alaska_Native_Population']\
#                        .map(lambda x: int_convert(x))
#pop_data['Asian_Population'] = pop_data['Asian_Population']\
#                        .map(lambda x: int_convert(x))
#pop_data['Native_Hawaiian_Pac_Islander_Population'] = \
#                        pop_data['Native_Hawaiian_Pac_Islander_Population']\
#                        .map(lambda x: int_convert(x))
#pop_data['Other_Race_Population'] = pop_data['Other_Race_Population']\
#                        .map(lambda x: int_convert(x))
    #Remove the duplicate zip code data from the population data
pop_data = pop_data.drop_duplicates('Zip_Code')    
    #Remove the extraneous comma from the zip code data
inc_data['Zip_Code'] = inc_data['Zip_Code'].map(lambda x: x.replace(',',''))
#    #Convert the median income data to integers
#inc_data['Median_Income'] = inc_data['Median_Income']\
#                        .map(lambda x: int_convert(x))

####Combining the datasets####
#This section does the final convergence of the existing dataset and the new
#data. 

    #Merge the two datasets that were pulled from the census data.
new_data = pd.merge(pop_data,inc_data,how = 'inner',on = 'Zip_Code')
    #Merge the just merged new data with the existing dataset. 
merged_data = pd.merge(existing_data,new_data,how = 'left',on = 'Zip_Code')
