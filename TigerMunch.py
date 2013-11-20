from flask import Flask, request, redirect
import twilio.twiml
from datetime import datetime
import urllib
from bs4 import BeautifulSoup
import os
from random import choice

# function that returns menu url based on dining hall input
def getMealUrl(str):   

   dhallcodes = {"ROMA":"01",
                "WILSON":"02",
                "BUTLER":"02",
                "FORBES":"03",
                "GRADCOLLEGE":"04",
                "CJL":"05",
                "WHITMAN":"08", }
   
   # replace dining hall name with number in url
   code = dhallcodes[str]   
   url = "http://facilities.princeton.edu/dining/_Foodpro/menu.asp?locationNum="+code
   return url;


# function that returns laundry url based on laundry room input
def getLaundryUrl(str):   

   laundryCodes = {
      "1903": "3073423",
      "1915": "3073425",
      "2D": "3073425",
      "BLAIR": "307342",
      "BLOOMBERG ": "3073427",
      "BLOOMBERG 269": "3073440",
      "BLOOMBERG 332": "3073441",
      "BLOOMBERG 460": "3073442",
      "BROWN": "3073475",
      "BUTLER D032": "3073463",
      "BUTLER A005": "3073462",
      "BUYERS": "3073444",
      "CLAPP": "307343",
      "DOD": "307344",
      "EDWARDS": "307345",
      "HAMILTON": "3073443",
      "HENRY": "3073410",
      "FEINBERG": "307346",
      "FORBES MAIN": "307347",
      "FORBES ANNEX": "307348",
      "HOLDER": "307349",
      "JOLINE": "3073411",
      "LAUGHLIN": "3073412",
      "LITTLE A49": "3073426",
      "LITTLE B6": "3073464",
      "LITTLE A5": "3073413",
      "LOCKHART": "3073428",
      "PATTON 4TH": "3073416",
      "PATTON BASEMENT": "3073415",
      "PYNE": "3073417",
      "SCULLY NORTH 2ND FLOOR": "3073418",
      "SCULLY SOUTH 1ST FLOOR": "3073419",
      "SCULLY SOUTH 4TH FLOOR": "3073420",
      "SPELMAN": "3073421",
      "WHITMAN A119": "3073465",
      "WHITMAN C205": "3073466",
      "WHITMAN C305": "3073467",
      "WHITMAN C407": "3073468",
      "WHITMAN F312": "3073470",
      "WHITMAN F403": "3073471",
      "WHITMAN FB11": "3073469",
      "WHITMAN S201": "3073472",
      "WHITMAN S301": "3073473",
      "WHITMAN S401": "3073474",
      "WITHERSPOON": "3073422"
      }
   
   
   # replace dining hall name with number in url
   code = laundryCodes[str]
   url = "http://www.laundryview.com/laundry_room.php?lr=" + code
   return url


# parses query and gets Laundry Status
def getLaundryStatus(str):
    # Get URL
    url = getLaundryUrl(str)
    
    # Fetch HTML
    f = urllib.urlopen(url)
    html = f.read()

    # Get BeautifulSoup Object
    soup = BeautifulSoup(html)

    laundryStatus = ""

    #parse url for the relevant statuses
    for appliance in soup.find_all(id="appliance_status"):
        laundryStatus+=appliance.get_text()

    # get rid of this sentence
    laundryStatus = laundryStatus.replace("Machine status will refresh in 60 seconds","")

    return str(laundryStatus)     

# function to abbreviate 
def shortenMeal(str):
   #dictionary of abbreviations 
   abbrlist = {"Breakfast": "Brkfst",
               "Chicken": "Chkn",
               "Scrambled Eggs": "Scrmbld Eggs",
               "Breakfast Sausage Patties": "Sausage Patties",
               "Gyro Bar Pita & Fillings": "Gyro Bar",
               "Gyro Beef Filling": "",
               "Vegan Gyro Filling": "",
               "Yukon Gold Mashed Potatoes": "Mashed Potatoes",
               "Mashed Potatoes": "Mshd Potatoes",
               "French Texas Toast": "French Toast",
               "CCC ": "",
               "Parmesan": "Parm.",
               "& Assorted": "&",
               "Assorted Breakfast Pastry": "Brkfst Pastries",
               "Baked ": "",
               "Fresh ": "",
               " with ": " & ",
               "Eggs Made to Order": "Eggs 2 Order",
               "Grilled Breakfast Potato": "Brkfst Potato",
               "Sliced ": "",
               "Fresh Hand Cut Idaho French Fries": "French Fries",
               "Italian Navy Bean Soup": "Bean Soup",
               "Forbes ": "",
               "Vegetables": "Veggies",
               "Vegetable": "Veg.",
               "with Bow Ties & Rigatoni": "",
               "Vegan Selections": "Vegan Bar",
               "Broccoli": "Brccli",
               "Grass Fed ": "",
               "Spinach": "Spnch",
               "Mushroom": "Mshrm",
               "Farmer's Ham": "Ham",
               "Quesadilla": "Qsdlla",
               "Taco Bar Fillings": "Taco Bar",
               "Catch of the Day": "Fish",
               "Taco Bar Fixins": "",
               "Herb Whipped": "Whipped",
               "Stroganoff": "Strog.",
               "Buttermilk Pancakes": "Pancakes",
               "Portobello": "Prtbllo",
               "Eggplant": "Eggplnt",
               "Sweet Corn": "Corn",
               "Tomato": "Tmto",
               "Grapefruit Half": "Grpefruit",
               "Pork Sausage Links": "Pork Sausages",
               "O'Brien": "",
               "Mexican": "Mex",
               "Shanghai": "",
               "Vietnamese": "Viet",
               "Road House": "",
               "Steelhead": "",
               "Cavatelli": "Cvtelli",
               "Tuscan ": "",
               "**College Theme Dinner @ Whitman Dining Hall**": ""}

   #iterate through dictionary replacing elements in string
   for k, v in abbrlist.iteritems():
      str = str.replace(k, v)

   # clean white lines
   str = "".join([s for s in str.splitlines(True) if s.strip("\r\n")])

   return str

# get next meal from time
def getNextMeal():
    hour = datetime.now().hour
    minute = datetime.now().minute

    # note the five hour offset

    if hour <= 1:
       return "Dinner"
    if hour <= 16:
        return "Breakfast"
    elif hour <= 19:
        return "Lunch"
    elif hour <= 24:
        return "Dinner"
    #elif hour <= 22:
#        return "Late Meal"

      
# prints meal from meals dictionary input and desired meal as string
def printMeal(meals, str):
    str = str.upper()
    # print name of dhall and meal
    print(meals["dhall"] + " " + str)
    # print menu
    print(meals[str])

# parses query and gets desired meal and dhall
def getMeals(str):
    # Get URL
    url = getMealUrl(str)
    
    # Fetch HTML
    f = urllib.urlopen(url)
    html = f.read()

    # Get BeautifulSoup Object
    soup = BeautifulSoup(html)

    # get list and length
    foodlist = soup.find_all('div') 
    length = len(foodlist)

    #create meal dictionary
    meals = dict()

    # create dhall name entry
    meals["dhall"] = str

    # go through and find all meals, and all foods in the meals
    for meal in soup.find_all('meal'):
        mealName =  meal['name'].upper()
        mealMenuList = ""
        for food in meal.find_all('name'):
            mealMenuList+=food.get_text() + "\n"
        meals[mealName] = shortenMeal(mealMenuList)

    return meals


def parse_query(query):
    dhall = ""
    meal = ""
    laundry = ""

    query = query.lower()
    
    #dhall dictionary
    dhalls   = {
       "wilson": "WILSON",
       "wu": "BUTLER",
       "wilcox": "WILSON",
       "wucox": "WILSON",
       "gryffindor": "WILSON",
       "gryfindor": "WILSON",
       "butler": "BUTLER",
       "muggle": "BUTLER",
       "hufflepuff": "FORBES",
       "forbes": "FORBES",
       "whitman": "WHITMAN",
       "slytherin": "WHITMAN",
       "rocky": "ROMA",
       "mathey": "ROMA",
       "roma": "ROMA",
       "rocky/mathey": "ROMA",
       "rockefeller": "ROMA",
       "ravenclaw": "ROMA",
       "nunokawa": "ROMA",
       "grad student": "GRADCOLLEGE",
       "graduate": "GRADCOLLEGE",
       "gradcollege":"GRADCOLLEGE",
       "cjl":"CJL",
       "jewish": "CJL",
       "sea jail": "CJL",
       "best rescollege ever": "WILSON"
       }

    # meal dictionary
    meals    = {
       "lunch": "Lunch",
       "breakfast": "Breakfast",
       "brunch": "Brunch",
       "dinner": "Dinner",
       "morning": "Breakfast",
       "afternoon": "Lunch",
       "tonight": "Dinner"
       }

    # laundry dictionary
    laundry_stations  = {
      "feinberg": "FEINBERG",
      "1903": "1903",
      "1915": "1915",
      "2D": "2D",
      "blair": "BLAIR",
      "bloomberg 041": "BLOOMBERG 041",
      "bloomberg 269": "BLOOMBERG 269",
      "bloomberg 332": "BLOOMBERG 332",
      "bloomberg 460": "BLOOMBERG 460",
      "brown": "BROWN",
      "d032": "BUTLER D032",
      "a005": "A005",
      "buyers": "BUYERS",
      "clapp": "CLAPP",
      "dod": "DOD",
      "edwards": "EDWARDS",
      "hamilton": "HAMILTON",
      "henry": "HENRY",
      "feinberg": "FEINBERG",
      "forbes main": "FORBES MAIN",
      "annex": "ANNEX",
      "holder": "HOLDER",
      "joline": "JOLINE",
      "laughlin": "LAUGHLIN",
      "little A49": "LITTLE A49",
      "little B6": "LITTLE B6",
      "little A5": "LITTLE A5",
      "lockhart": "LOCKHART",
      "patton 4th": "PATTON 4TH",
      "patton basement": "PATTON BASEMENT",
      "pyne": "PYNE",
      "SCULLY NORTH 2ND FLOOR": "SCULLY NORTH 2ND FLOOR",
      "SCULLY SOUTH 1ST FLOOR": "SCULLY SOUTH 1ST FLOOR",
      "SCULLY SOUTH 4TH FLOOR": "SCULLY SOUTH 4TH FLOOR",
      "spelman": "SPELMAN",
      "a119": "WHITMAN A119",
      "c205": "WHITMAN C205",
      "c305": "WHITMAN C305",
      "c407": "WHITMAN C407",
      "f312": "WHITMAN F312",
      "f403": "WHITMAN F403",
      "fb11": "WHITMAN FB11",
      "s201": "WHITMAN S201",
      "s301": "WHITMAN S301",
      "s401": "WHITMAN S401",
      "spoon": "WITHERSPOON",
      "witherspoon": "WITHERSPOON" 
       }
    
    # greetings
    greetings    = {
       "hi": "hi",
       "what's up": "hi",
       "whats up": "hi",
       "hey": "hi",
       "yo": "hi",
       "sup": "hi",
       }

    # exception cases
    exception_cases = {
       "what is the time": "hour",
       "what time is it": "hour",
       "who made this app": "Why, it was Nihar, of course! Nihar is awesome.",
       }

    #dhall case
    for key in dhalls:
        if key in query:
            type = "food"
            dhall = dhalls[key]

             # search for meal
            for key in meals:
                 if key in query:
                     meal = meals[key]

             # no specified meal - get next meal function
            if meal == "":
                 meal = getNextMeal()
                 if meal == "Late Meal":
                    return ["exception", "Go get late meal!"]
        
            return [type, dhall, meal]

    # greeting case
    for key in greetings:
       if key in query:
          type = "greeting"
          return[type]

    # exception cases
    for key in exception_cases:
       if key in query:
          type = "exception"
          exception_value = exception_cases[key]
          # time case
          if exception_value == "hour":
             exception_value = str(datetime.now())
          return[type, exception_value]
         
    # no specified dhall
    if dhall == "":
        type = "exception"
        exception_name = "Specify a dining hall and meal! Example: 'wilson dinner'"
        return[type, exception_name]

app = Flask(__name__)


def greeting(from_number):
   
    # List of known callers
    callers = {
     "+16783602442": "Nihar",
    }

    if from_number in callers:
       name = callers[from_number]
       message = "Hi " + name + "! \n"

       if name == "Nihar":
          message = "Aww, are you my creator? That's so sweet! Thanks for making me! You're the coolest person ever!!!"
          
    else:
       message = "hi!!!"
    
    return message

@app.route("/", methods=['GET', 'POST'])
def send_text():
    resp = twilio.twiml.Response()

    # get from and body
    from_number = request.values.get('From', None)
    query = request.values.get('Body', None)

    message = ""
    
    #parse query
    parsedArray = parse_query(query)
    if (parsedArray[0] == "exception"):
        response = parsedArray[1]
    elif (parsedArray[0] == "greeting"):
        response = greeting(from_number)
    elif (parsedArray[0] == "food"):       
        # pass dhall to getMeals and get dictionary
        meals = getMeals(parsedArray[1])
        # pass dictionary and desired meal to printmeal to print
        # print name of dhall and meal
        meal = parsedArray[2].upper() #capitalized meal
        response = (meals["dhall"] + " " + meal + "\n")
        # print menu
        response+=meals[meal]
    elif (parsedArray[0] == "laundry"):
        laundryStatus = getLaundryStatus(parsedArray[1])
        response = (parsedArray[1] + ": ")
        response += laundryStatus
    else:
       response = "error"

    message+=response
    
    #handle long message case
    if len(message) > 160:
       resp.sms("(1)\n" + message[:156])
       resp.sms("(2)\n" + message[156:312])          
       if len(message) > 312:
          resp.sms("(3)\n" + message[312:468])          

    else:
       resp.sms(message)
 
    return str(resp)
   
 
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
