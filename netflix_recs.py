"""
Filter Netflix movies using multiple criteria based on Rotten Tomatoes's critics and user ratings
1) Get list of Netflix movies from database
2) Search each movie on Rotten Tomatoes by appending '/m/movie_title' to www.rottentomatoes.com
3) Store ratings such as critics rating and audience score into a dictionary
4) Allow user to filter dictionary based on certain criteria (etc. more than 70% Tomatoemeter score, or more than $1 million box office)
6) Print the resulting movies and provide the rotten tomatoe links
"""

from bs4 import BeautifulSoup
import urllib.request

url = urllib.request.urlopen("https://www.pastemagazine.com/articles/2016/06/the-100-best-movies-on-netflix-june-2016.html?a=1").read()
soup = BeautifulSoup(url,"xml")
movies = {} #searchable dictionary 

def tomato_url(movie):
    """strip unnecessary punctuation from movie titles"""
    punctuation = [33,34,39,44,45,58,59]
    newmovie = movie
    for character in movie:
        if ord(character) in punctuation: 
            newmovie = movie.replace(character,"") #delete punctuation
    return newmovie

def get_rating(address,title):
    """pull ratings numbers from rotten tomatoes"""
    x = address.encode('ascii','ignore') #ignore encoded characters outside of the range for ascii chars
    nx = x.decode('ascii')
    while True:
        try:
            RTaddress = urllib.request.urlopen(nx)
            tomatoe = BeautifulSoup(RTaddress, "lxml")
            audiencescore = tomatoe.find('span',class_="superPageFontColor",style="vertical-align:top")
            criticscore = tomatoe.select('span.meter-value > span')[0]
            criticsrating = criticscore.get_text() + "%"
            audiencerating = audiencescore.get_text()
            movies[title]={"critics":criticsrating,"audience":audiencerating}
            break
        except IndexError:
            print("oops, there's no rating available for this title:" + title)
            break
        except urllib.error.HTTPError:
            print("oops, I can't find that title's web address:" + title)
            break
              
print("Please wait while we are loading our database")

def filter_movies(num):
    if num == "1":
        critics_choice = input("How low will you go on a rating scale from 0 to 100?")
        goodtitles = {key: value['critics'] for (key, value) in movies.items() if value['critics'].rstrip("%") > critics_choice}
        print(goodtitles)

    elif num == "2":
        audience_choice = input("How low will you go on a rating scale from 0 to 100?")
        goodtitles = {key: value['audience'] for (key, value) in movies.items() if value['audience'] > audience_choice}
        print(goodtitles)
        
    else: 
        try_again = input("oops, you didn't enter 1 (critics rating) or 2 (audience rating). Please try again")
        filter_movies(try_again)

#PROGRAM STARTS HERE 
for movie in soup.find_all('a', class_="ovr"):
    netflix_link = movie.get('href')
    if "www.netflix.com" in netflix_link: 
        lowercase = ''.join(movie.find_all(text=True)).lower().replace(" ","_")
        RT = tomato_url(lowercase) #movie title sanitation
        RTlink = 'https://www.rottentomatoes.com/m/' + RT
        get_rating(RTlink,RT)

###USER INTERFACE###

while True:
    criteria = input("Enter the number corresponding to how you would like to filter movies\n1)Critics Score\n2)Audience Score")
    filter_movies(criteria)
    more = input("Want more recommendations from Rotten Tomatoes (Y/N)?")
    if more =="N":
        break;
            
        
        
        





    
                          
        
         
         





        

