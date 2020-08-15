import requests
from bs4 import BeautifulSoup
import custom

class scraper_program(object):

    def __init__(self):
        self.search_term = ""
        self.search_location = ""
        self.job_elems = ""

    def new_search(self):
        self.search_term = parser("Please enter a search term: ").to_URL()
        self.search_location = parser("Please enter desired location: ").to_URL()

        URL = 'https://www.monster.com/jobs/search/?q='+self.search_term+'&where='+self.search_location
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser') # beautiful soup instantiation, page.content contains HTML code of URL address
        results = soup.find(id='ResultsContainer')

        self.job_elems = results.find_all('section', class_='card-content')
        i=0

        for job_elem in self.job_elems:
            title_elem = job_elem.find('h2', class_='title')
            company_elem = job_elem.find('div', class_='company')
            location_elem = job_elem.find('div', class_='location')
            if None in (title_elem, company_elem, location_elem):
                continue
            print("["+str(i)+"] "+title_elem.text.strip())
            print(company_elem.text.strip())
            print(location_elem.text.strip())
            print()
            i+=1

        chosen_index = custom.parser("Choose a function [apply 'index_of_desired_job' / new]: ").function(self)

    def get_application_address(self, params):
        if len(params) == 1 and params[0].isnumeric():
            index = int(params[0])
            i=0
            for job_elem in self.job_elems:
                if i != index:
                    i+=1
                    continue
                title_elem = job_elem.find('h2', class_='title')
                company_elem = job_elem.find('div', class_='company')
                location_elem = job_elem.find('div', class_='location')
                if None in (title_elem, company_elem, location_elem):
                    continue
                link = job_elem.find('a')['href']
                if link == None:
                    print("Could not acquire link.")
                    continue
                print()
                print(f"Apply here: {link}\n")
                print()
                i+=1
        else:
            print("Invalid command!")

        chosen_index = custom.parser("Choose a function [apply 'index_of_desired_job' / new]: ").function(self)

class parser(object):
    """a (not-so) fancy-shmancy string parser for ui"""
    def __init__(self, prompt):
        self.string = input(prompt)

    def to_URL(self):
        ret = self.string.replace(" ","-")
        return ret

    def function(self, program):
        validated = False
        while validated == False:
            parameter_arr = self.string.lower().split()
            command = parameter_arr.pop(0)
            cmd_dictionary = {
                'new':program.new_search,
                'apply':program.get_application_address
                }
            if cmd_dictionary.get(command) != None:
                validated = True
                if len(parameter_arr) != 0 and command != "new":
                    cmd_dictionary[command](parameter_arr)
                else:
                    cmd_dictionary[command]()
            else:
                self.string = input("Invalid command!\n\nChoose a function [apply 'index_of_desired_job' / new]: ")
                continue
