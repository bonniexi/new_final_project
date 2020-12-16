from bs4 import BeautifulSoup
import requests
import json
import secrets  # file that contains your API key
import time
import sqlite3


BASE_URL_1 = "https://www.lib.umich.edu"
BASE_URL_2 = "https://www.lib.umich.edu/locations-and-hours"

CACHE_FILENAME = "final_project_cache.json"
CACHE_DICT = {}

# Part 1: Cache functions

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk

    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    '''
    cache_file = open(CACHE_FILENAME, 'w')
    contents_to_write = json.dumps(cache_dict)
    cache_file.write(contents_to_write)
    cache_file.close()


def make_request_with_cache_text(url):
    '''Check the cache for a saved result for this url.
    If the result is found, print "Using Cache" and return it.
    Otherwise send a new request, print "Fetching", save it, then return it.

    Parameters
    ----------
    url: string

    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache

    '''
    if url in CACHE_DICT.keys():
        print("Using Cache")
        return CACHE_DICT[url]
    else:
        print("Fetching")
        time.sleep(1)
        CACHE_DICT[url] = requests.get(url).text
        save_cache(CACHE_DICT)
        return CACHE_DICT[url]


CACHE_DICT = open_cache()

# Part 2: Implement UmichLibrary class

class UmichLibrary:
    '''a library in University of Michigan

    Instance Attributes
    -------------------
    name: string
        the name of a library

    location: string
        the location of a library

    hours: string
        the hours of a library

    phone: string
        the phone of a library
    '''

    def __init__(self, name, intro, location):

        self.name = name
        self.intro = intro
        self.location = location

    def info(self):
        return f"{self.name} locates at {self.location}. {self.intro}"

# Part 3: Scrape html to get libraries' infomation

def build_library_url_dict():
    ''' Make a dictionary that maps library name to library page url from "https://www.lib.umich.edu/locations-and-hours"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''
    library_name_url_dict = {}
    # Make the soup
    response = make_request_with_cache_text(BASE_URL_2)
    soup = BeautifulSoup(response, "html.parser")
    # For each library listed
    library_list = soup.find_all(
        'li', class_="css-77qsxv")

    for item in library_list:
        library_link = item.find('a')['href']
        library_name = item.find('span').text
        library_name_url_dict[library_name.lower()] = BASE_URL_1 + library_link

    return library_name_url_dict


def get_library_instance(library_url):
    '''Make an instances from a library URL.

    Parameters
    ----------
    library_url: string
        The URL for a library page

    Returns
    -------
    instance
        a UmichLibrary instance
    '''

    response = make_request_with_cache_text(library_url)
    soup = BeautifulSoup(response, "html.parser")
    library_name = soup.find(
        'h1', class_="css-1xx2irx-StyledHeading e1tlxttt0").text
    library_intro = soup.find(
        'p', class_="css-733d4y-StyledText ettiaw90").text
    library_address = soup.find('address').text.split('Address')[1].split('View')[0]
    error_cause = "Building 18, Room G018"
    if error_cause in library_address:
        library_address.replace(error_cause, ' ')
    return UmichLibrary(library_name, library_intro, library_address)

# Part 4: Request restaurants' information from YELP! API

def get_nearby_restaurants(library_object):
    '''Obtain API data from YELP! API. Check the cache for a saved result for this resource_url + params:values
    combo. If the result is found, print "Using Cache" and return it. Otherwise send a new request,print "Fetching",
    save it, then return it.

    Parameters
    ----------
    library_object: object
        an instance of a national site

    Returns
    -------
    dict
        a converted API return from YELP! API
    '''
    resource_url = 'https://api.yelp.com/v3/businesses/search'
    param_strings = []
    connector = '_'
    
    headers = {'Authorization': 'Bearer %s' % secrets.YELP_FUSION_API_KEY}
    params = {'location': library_object.location, 'term': 'restaurants', 'radius': 1000, 'limit': 10}

    for k in params.keys():
        param_strings.append(f'{k}={params[k]}')
    param_strings.sort()
    unique_key = resource_url + '?' + connector.join(param_strings)

    if unique_key in CACHE_DICT.keys():
        print("Using Cache")
        return CACHE_DICT[unique_key]
    else:
        print("Fetching")
        time.sleep(1)
        CACHE_DICT[unique_key] = requests.get(resource_url, params=params, headers=headers).json()
        save_cache(CACHE_DICT)
        return CACHE_DICT[unique_key]


CACHE_DICT = open_cache()

# Part 5: Interaction 

if __name__ == "__main__":

    library_name_url_dict = build_library_url_dict()
    while True:
        want_to_study_in_library = input("Do you want to study in library? Please enter 'yes' or 'no' ('no' means exiting this program): ")
        if want_to_study_in_library == 'yes':
            num_0 = 0
            num_lib_dict = {}
            for key in library_name_url_dict.keys():
                num_0 += 1
                num_lib_dict[num_0] = key
                print(f"[{num_0}] {key}")
            while True:
                wanted_library = input(
                    "Enter the number of the library where you want to study or “exit”: ")
                if wanted_library == "exit":
                    exit()
                elif wanted_library.isdigit():
                    if int(wanted_library) in range(1, 17):
                        wanted_library_name = num_lib_dict[int(wanted_library)]
                        for key, value in library_name_url_dict.items():
                            if key == wanted_library_name:
                                library_url = value
                                umich_library_instances = get_library_instance(library_url)
                                print(umich_library_instances.info())

                                while True:
                                    if_know_more = input("Know more about the nearby restaurants, “yes” or “exit” or “back”?")
                                    if if_know_more == "exit":
                                        exit()
                                    elif if_know_more == "back":
                                        break
                                    elif if_know_more == "yes":
                                        print('-'*42)
                                        print(f"List of restaurants nearby {wanted_library_name}")
                                        print('-'*42)
                                        restaurants_results = get_nearby_restaurants(umich_library_instances)['businesses']
                                        if restaurants_results:
                                            num_res_dict = {}
                                            num = 0
                                            for item in restaurants_results:
                                                num += 1
                                                num_res_dict[num] = item
                                                res_name = item['name']
                                                print("["+str(num)+"]"+" "+res_name)
                                            while True:
                                                wanted_num = input("Please choose the number of your favorite restaurant for more details or “exit” or “back”: ")
                                                if wanted_num == 'exit':
                                                    exit()
                                                elif wanted_num == 'back':
                                                    break
                                                elif wanted_num.isdigit():
                                                    if int(wanted_num) in range(1, int(num)+1):
                                                        res_name = num_res_dict[int(wanted_num)]['name']
                                                        res_rating_level = num_res_dict[int(wanted_num)]['rating']
                                                        res_location = num_res_dict[int(wanted_num)]['location']['display_address'][0]
                                                        res_phone = num_res_dict[int(wanted_num)]['display_phone']
                                                        res_url = num_res_dict[int(wanted_num)]['url']
                                                        print(f"{res_name} locates at {res_location}.")
                                                        print(f"Its rating level is {res_rating_level}.")
                                                        print(f"Please contact {res_phone} for more information.")
                                                        print(f"You can also navigate to this restaurant's url to learn more: {res_url}")

                                                    else:
                                                        print("[ERROR] Invalid input.")
                                                        print()
                                                        continue
                                                else:
                                                    print("[ERROR] Invalid input.")
                                                    print()
                                                    continue   
                                        else:
                                            print("No restaurants nearby! Why not study at other libraries?")
                                            print()
                                            break                   

                                    else:
                                        print("[ERROR] Invalid input.")
                                        print()
                                        continue
                    else:
                        print("[ERROR] Invalid input.")
                        print()
                        continue
                else:
                    print("[ERROR] Invalid input.")
                    print()
                    continue
        elif want_to_study_in_library == 'no':
            exit()
        else:
            print('Please choose between yes and no')
            print()
            continue        
                