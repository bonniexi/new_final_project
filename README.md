# new_final_project


## Install

requests  
sqlite3  
BeautifulSoup  
time


## Usage

This project contains two code files to run:  
final_project_code.py 
database_code.py

### Get YELP! API Key

This prject needs API Key from YELP!. You could navigate to https://www.yelp.com/developers/documentation/v3/authentication, then click on the "Create App" link. It will take you to the login page. Login with your account details. You will find your API key under General > Manage App. You can enter your email ID and description on this page. Copy this API key in a safeplace.

### How to Run final_project_code

At the beginning, import the file that contains your API key (in my code, it is secrets.py).  
This file includes five parts: cache functions, UmichLibrary class, scrape html to get libraries' infomation, request restaurants' information from API, and interaction.  
The interaction part starts with entering a library name you want to study at, then the program will provide the name, location and short introduction of this library. After that, you could choose to know more about the nearby restaurants, or go back to last question, or end this program. If you say "yes", the program will show you 10 restuarants near your selected library. Then you could choose the number of your favourite restaurant in the list, or go back to last question, or end this program. If you have chosen the number, the program will tell you the location, rating, the phone of this restaurant and the url of this restaurant.

### How to Run database_code

At the beginning, import the final_project_code file to use the functions there.  
This file include two parts: create a dictionary to save all the needed information, create databse with two tables. 


## License
UMICH @ Chang Gao (U-M ID: 18554062)
