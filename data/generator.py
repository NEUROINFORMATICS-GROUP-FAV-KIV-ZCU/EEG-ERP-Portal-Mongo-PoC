__author__ = 'veveri'

from data.classes import *
from pprint import pprint

def generate_persons(firstname_count, lastname_count):
    firstnameConst = "firstname"
    lastnameConst = "lastname"

    persons = []

    for i in range(0, lastname_count):
        lastname = lastnameConst + str(i)
        for j in range(0, firstname_count):
            firstname = firstnameConst + str(j)
            persons.append(person(firstname, lastname))

    return persons

def generate_research_groups(title_count, owners):
    titleConst = "researchGroup"
    descConst = "researchGroupDescription"

    own_count = len(owners)

    groups = []
    own_index = -1
    for i in range(0, title_count):
        own_index = (own_index + 1) % own_count
        title = titleConst + str(i)
        desc = descConst + str(i)

        groups.append(research_group(owners[own_index],title, desc))

    return groups
