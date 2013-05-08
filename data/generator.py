__author__ = 'Jakub Danek'

from data.classes import *
import oracle as oc

### GLOBALS###########################################
firstnameConst = "firstname"     #person firstname
lastnameConst = "lastname"       #person lastname

### DATABASE INIT#####################################
def init_oracle(lastname_count, firstname_count, group_count, scenario_count_per_group, artefact_count, weather_count, subj_group_count, digit_count, electrode_count):
    oc.clear_db()
    print "DB is empty now"

    #generate electrode_systems
    elect = generate_electrode_systems(electrode_count)
    oc.save_electrode_system(elect)
    print "Electrode Systems generated"

    #generate artefacts
    arts = generate_artefacts(artefact_count)
    oc.save_artefacts(arts)
    print "Artefacts generated"

    #generate digitizations
    digits = generate_digitizations(digit_count)
    oc.save_digitalization(digits)
    print "Digitizations generated"

    #generate weather info
    weathers = generate_weathers(weather_count)
    oc.save_weather(weathers)
    print "Weathers generated"

    #generate subj. groups
    subj_groups = generate_subject_groups(subj_group_count)
    oc.save_subject_group(subj_groups)
    print "Subject groups generated"

    #generate persons
    pers = generate_persons(firstname_count, lastname_count)
    oc.save_persons(pers)
    print "Persons generated"

    #generate groups, owners differ by lastname
    pers = oc.query_persons(oc.person_select_by_firstname, [firstnameConst + '0'])
    groups = generate_research_groups(group_count, pers)
    oc.save_research_groups(groups)
    groups = oc.query_groups(oc.research_group_select_all)
    print "Research groups generated"

    #add members to groups
    for g in groups:
        pers = oc.query_persons(oc.person_select_by_lastname, [g.owner.lastname])
        oc.add_res_group_members(g, pers)
    print "Research group members added"

    #add scenarios to groups
    scenarios = generate_scenarios(scenario_count_per_group, groups)
    oc.save_scenarios(scenarios)
    print "Scenarios generated"

def generate_experiments(exp_per_member = 10):
    oc.clear_experients()

    subj_groups = oc.query_subject_groups(oc.subject_group_select_all)
    subj_grp_len = len(subj_groups)
    subj_grp_index = 1
    print "Subject groups loaded"
    subjects = oc.query_persons(oc.person_select_all)
    subj_len = len(subjects)
    subj_index = 22
    print "Subjects loaded"
    #scenarios = oc.query_scenarios(oc.scenario_select_all)
    scenarios = oc.query_scenarios_full(oc.scenario_select_all_full)
    scenario_len = len(scenarios)
    scenario_index = 34
    print "Scenarios loaded"
    weathers = oc.query_weathers(oc.weather_select_all)
    weather_len = len(weathers)
    weather_index = 53
    print "Weather loaded"
    artefacts = oc.query_artefacts(oc.artefact_select_all)
    artefact_len = len(artefacts)
    artefact_index = 76
    print "Artefacts loaded"
    electrodes = oc.query_electrode_confs(oc.electrode_conf_select_all)
    electrode_len = len(electrodes)
    electrode_index = 92
    print "Electrode configurations loaded"
    digits = oc.query_digitizations(oc.digitization_select_all)
    digit_len = len(digits)
    digit_index = 17
    print "Digitizations loaded"
    groups = oc.query_groups(oc.research_group_select_all)
    print "Research roups loaded"
    exps = []
    print "Starting to generate experiments."
    for g in groups:
        members = oc.query_persons(oc.research_group_member_select_by_group, [(g.id)])
        for m in members:
            for i in range(0, exp_per_member):
                exp = experiment()
                exp.owner = m
                exp.research_group = g
                exp.subject, subj_index = get_item_from_dict(subjects, subj_index, subj_len)
                exp.subject_group, subj_grp_index = get_item_from_dict(subj_groups, subj_grp_index, subj_grp_len)
                exp.scenario, scenario_index = get_item_from_dict(scenarios, scenario_index, scenario_len)
                exp.weather, weather_index = get_item_from_dict(weathers, weather_index, weather_len)
                exp.artefact, artefact_index = get_item_from_dict(artefacts, artefact_index, artefact_len)
                exp.electrode, electrode_index = get_item_from_dict(electrodes, electrode_index, electrode_len)
                exp.digitization, digit_index = get_item_from_dict(digits, digit_index, digit_len)
                exps.append(exp)
    print "Experiments generated, insering into DB"
    oc.save_experiments(exps)
    print "Experiments saved in the DB"

def get_item_from_dict(dict, index, length):
    return dict[index], (index + 1) % length



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