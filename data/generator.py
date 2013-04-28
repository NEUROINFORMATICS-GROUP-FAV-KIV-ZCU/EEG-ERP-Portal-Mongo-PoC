__author__ = 'veveri'

from data.classes import *
import oracle as oc

### GLOBALS###########################################
firstnameConst = "firstname"
lastnameConst = "lastname"

### DATABASE INIT#####################################
def init_oracle(lastname_count, firstname_count, group_count, scenario_count_per_group, artefact_count):
    oc.clear_db()

    #generate artefacts
    arts = generate_artefacts(artefact_count)
    oc.save_artefacts(arts)

    #generate persons
    pers = generate_persons(firstname_count, lastname_count)
    oc.save_persons(pers)

    #generate groups, owners differ by lastname
    pers = oc.query_persons(oc.person_select_by_firstname, [firstnameConst + '0'])
    groups = generate_research_groups(group_count, pers)
    oc.save_research_groups(groups)
    groups = oc.query_groups(oc.research_group_select_all)

    #add members to groups
    for g in groups:
        pers = oc.query_persons(oc.person_select_by_lastname, [g.owner.lastname])
        oc.add_res_group_members(g, pers)

    #add scenarios to groups
    scenarios = generate_scenarios(scenario_count_per_group, groups)
    oc.save_scenarios(scenarios)

### DATA GENERATORS###################################
def generate_persons(firstname_count, lastname_count):
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