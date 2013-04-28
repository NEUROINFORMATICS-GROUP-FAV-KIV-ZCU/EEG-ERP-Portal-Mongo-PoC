__author__ = 'veveri'

from data.classes import *

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

def generate_scenarios(title_count_per_group, groups):
    titleConst = "scenario"
    descConst = "scenarioDescription"

    scenarios = []
    i = 0
    for g in groups:
        for j in range(0, title_count_per_group):
            title = titleConst + str(i)
            desc = descConst + str(i)

            scenarios.append(scenario(g.owner, g, title, desc))
            i += 1

    return scenarios

def generate_artefacts(compensation_count, reject_param=5):
    compensation_const = "compensation"
    reject_const = "reject"
    artefacts = []
    for i in range(0, compensation_count):
        compensation = compensation_const + str(i)
        reject = reject_const + str(i % reject_param)
        artefacts.append(artefact(compensation, reject))

    return artefacts