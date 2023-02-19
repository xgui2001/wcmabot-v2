import os
import random
import pandas as pd
import json
import requests

wcma_url = 'https://artmuseum.williams.edu/collection/'

# import WCMA collection data from csv file and stores it with a Pandas dataframe


def get_collection():
    data_dir = os.getcwd()+'/collection'
    collection_df = pd.read_csv(
        data_dir+'/wcma-collection.csv', low_memory=False)
    return collection_df


# generate a tweet that describes an object from the WCMA dataframe
def generate_object():
    random_int = random.randint(0, len(get_collection()))
    image_url = "https://get-thumb.herokuapp.com/getThumbLarge.php?objectid=" + \
        str(random_int)
    random_object = get_collection().iloc[random_int]
    # one tweet has title, maker, creation date, medium and department
    object_string = str(random_object[1]) + ', ' + str(random_object[2]) + ', ' + str(random_object[7]) + \
        ', ' + str(random_object[12]) + ', ' + str(random_object[4])
    # check if image page is valid, if so add the image url to the string
    image_page = requests.get(image_url)
    if image_page.status_code == 200:
        object_string += '\nObject Image: '+image_url
    else:
        object_string += ''+wcma_url
    print(object_string)
    return object_string
