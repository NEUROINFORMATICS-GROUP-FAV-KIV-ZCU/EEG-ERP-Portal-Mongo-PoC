__author__ = 'Jakub Danek'

from data.classes import *
import oracle as oc

### GLOBALS###########################################
firstnameConst = "firstname"     #person firstname
lastnameConst = "lastname"       #person lastname

### DATABASE INIT#####################################
def init_oracle(lastname_count, firstname_count, group_count, scenario_count_per_group, artefact_count, weather_count, subj_group_count, digit_count, electrode_count):
    oc.clear_db()

    #generate electrode_systems
    elect = generate_electrode_systems(electrode_count)
    oc.save_electrode_system(elect)

    #generate artefacts
    arts = generate_artefacts(artefact_count)
    oc.save_artefacts(arts)

    #generate digitizations
    digits = generate_digitizations(digit_count)
    oc.save_digitalization(digits)

    #generate weather info
    weathers = generate_weathers(weather_count)
    oc.save_weather(weathers)

    #generate subj. groups
    subj_groups = generate_subject_groups(subj_group_count)
    oc.save_subject_group(subj_groups)

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

def generate_weathers(title_count):
    title_const = "weather"
    desc_const = "weather description"
    weathers = []
    for i in range(0, title_count):
        title = title_const + str(i)
        desc = desc_const + str(i)
        weathers.append(weather(title, desc))

    return weathers

def generate_subject_groups(title_count):
    title_const = "subject_group"
    desc_const = "subject_group description"
    subject_groups = []
    for i in range(0, title_count):
        title = title_const + str(i)
        desc = desc_const + str(i)
        subject_groups.append(subject_group(title, desc))

    return subject_groups

def generate_digitizations(digi_count = 0):
    gain = 0
    sample = 10000
    filter_const = "filter"

    digits = []
    for i in range(0, digi_count):
        gain += 0.1
        sample += 1000
        filter = filter_const + str(i)

        digits.append(digitization(gain, filter, sample))

    return digits

def generate_electrode_systems(title_count):
    title_const = "electrode_system"
    desc_const = "electrode_system description"
    electrode_systems = []
    for i in range(0, title_count):
        title = title_const + str(i)
        desc = desc_const + str(i)
        electrode_systems.append(electrode_system(title, desc))

    return electrode_systems