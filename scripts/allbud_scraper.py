import bs4 as bs
import urllib.request
import json
from datetime import datetime
import gevent
from gevent import monkey
monkey.patch_all()

'''
    scrape data from allbud.com
'''


def do_scrape():
    results_acc = {}
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    for letter in alphabet:
        results_acc = scrape_for_letter(letter, results_acc)

    with open('../data/allbud_output.json', 'w') as outfile:
        json.dump(results_acc, outfile)


def scrape_for_letter(letter, results_dict):
    baseurl = 'https://www.allbud.com/marijuana-strains/search?sort=alphabet&letter='
    resultsurl = '&results=' + str(1000)
    allbudurl = 'https://www.allbud.com'


    start_time = datetime.now()
    count_per_letter = 0
    source = urllib.request.urlopen(baseurl + letter + resultsurl).read()
    soup = bs.BeautifulSoup(source,'lxml')

    mydivs = soup.findAll("article", {"class": "infocard strain"})

    # for each strain
    for div in mydivs:
        count_per_letter += 1
        name = div.find("h3", {"itemprop": "name"}).get_text().strip()
        try:
            rating = div.find("div", {"itemprop": "ratingValue"}).get_text().strip()
        except AttributeError:
            rating = None

        strainurl = div.find("section", {"class": "object-title"}).find("a", href=True)['href']

        strain_source = urllib.request.urlopen(allbudurl + strainurl).read()
        strain_soup = bs.BeautifulSoup(strain_source, 'lxml')

        pos_effects = strain_soup.find("section", {"id": "positive-effects"}).find_all("a", href=True)
        pos_effects_list = []
        for effect in pos_effects:
            pos_effects_list.append(effect.get_text())

        relieved_effects = strain_soup.find("section", {"id": "relieved"}).find_all("a", href=True)
        relieved_effects_list = []
        for effect in relieved_effects:
            relieved_effects_list.append(effect.get_text())

        flavor_effects = strain_soup.find("section", {"id": "flavors"}).find_all("a", href=True)
        flavor_effects_list = []
        for effect in flavor_effects:
            flavor_effects_list.append(effect.get_text())

        aroma_effects = strain_soup.find("section", {"id": "aromas"}).find_all("a", href=True)
        aroma_effects_list = []
        for effect in aroma_effects:
            aroma_effects_list.append(effect.get_text())

        description = strain_soup.find("div", {"class": "panel-body well description"}). \
            find("span", {"class": "hidden-xs"}, recursive=False).get_text().strip()
        #replace bad quotations and en dash with hyphen
        description = description.replace('\u201c','\"'). \
            replace('\u201d','\"').replace('\u2019','\''). \
            replace('\u2013','-')

        percentages_dict = {}
        percent_wrapper = strain_soup.find("h4", {"class": "percentage"})

        percentages = percent_wrapper.text.replace(" ", "").replace("\n", "").split(',')
        if percentages != ['']:
            for percentage in percentages:
                temp = percentage.split(':')
                percentages_dict[temp[0]] = temp[1]


        results_dict[name] = {
            'rating': rating,
            'positive': pos_effects_list,
            'medical': relieved_effects_list,
            'flavor': flavor_effects_list,
            'aroma': aroma_effects_list,
            'percentages': percentages_dict,
            'description': description
        }

    print('done with: ' + letter, ' with ' + str(count_per_letter) + ' strains')
    print(datetime.now() - start_time)

    return results_dict

def change_to_list_format():
    allbud_data = {}
    new_allbud_data = []
    with open('../data/allbud_output.json', encoding="utf8") as f:
        allbud_data = json.load(f)

    for key in allbud_data.keys():
        val = allbud_data[key]
        val["name"] = key
        new_allbud_data.append(val)

    with open('../data/allbud_output.json', 'w') as outfile:
        json.dump(new_allbud_data, outfile)

if __name__ == "__main__":
    do_scrape()
    change_to_list_format()
