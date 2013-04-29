__author__ = 'Jakub Danek'

import cx_Oracle
import utils as ut
from data.classes import *

### PERSON QUERIES##########################################
person_attributes = "GIVENNAME, SURNAME, GENDER, LATERALITY, EDUCATION_LEVEL_ID"
person_attributes_with_id = "PERSON_ID, " + person_attributes
person_insert = 'INSERT INTO PERSON(' + person_attributes + ') values(:1, :2, :3, :4, :5)'
person_select_all = "SELECT "  + person_attributes_with_id + " FROM PERSON"
person_select_by_id = person_select_all + " WHERE PERSON_ID = :1"
person_select_by_lastname = person_select_all + " WHERE SURNAME = :1"
person_select_by_firstname = person_select_all + " WHERE GIVENNAME = :1"
person_clear = "DELETE FROM PERSON"

### RESEARCH GROUP QUERIES#################################
research_group_attributes = "TITLE, DESCRIPTION, OWNER_ID"
research_group_attributes_with_id = "RESEARCH_GROUP_ID, " + research_group_attributes
research_group_insert = "INSERT INTO RESEARCH_GROUP(" + research_group_attributes +") VALUES(:1, :2, :3)"
research_group_select_all = "SELECT " + research_group_attributes_with_id + " FROM RESEARCH_GROUP"
research_group_select_by_id = research_group_select_all + " WHERE RESEARCH_GROUP_ID = :1"
research_group_clear = "DELETE FROM RESEARCH_GROUP"

research_group_member_attributes = "PERSON_ID, RESEARCH_GROUP_ID, AUTHORITY"
research_group_member_insert = "INSERT INTO RESEARCH_GROUP_MEMBERSHIP (" + research_group_member_attributes + ") VALUES (:1, :2, :3)"
research_group_member_clear = "DELETE FROM RESEARCH_GROUP_MEMBERSHIP"

### SCENARIO QUERIES#######################################
scenario_attributes = "TITLE, DESCRIPTION, OWNER_ID, RESEARCH_GROUP_ID"
scenario_attributes_with_id = "SCENARIO_ID, " + scenario_attributes
scenario_insert = "INSERT INTO SCENARIO(" + scenario_attributes + ") values (:1, :2, :3, :4)"
scenario_select_all = "SELECT " + scenario_attributes_with_id + " FROM SCENARIO"
scenario_clear = "DELETE FROM SCENARIO"

### ARTEFACT QUERIES#######################################
artefact_attributes = "COMPENSATION, REJECT_CONDITION"
artefact_attributes_with_id = "ARTEFACT_ID, " + artefact_attributes
artefact_insert = "INSERT INTO ARTEFACT(" + artefact_attributes + ") VALUES (:1, :2)"
artefact_select_all = "SELECT " + artefact_attributes_with_id + " FROM ARTEFACT"
artefact_clear = "DELETE FROM ARTEFACT"

### WEATHER QUERIES########################################
weather_attributes = "TITLE, DESCRIPTION"
weather_attributes_with_id = "WEATHER_ID, " + weather_attributes
weather_insert = "INSERT INTO WEATHER(" + weather_attributes + ") values (:1, :2)"
weather_select_all = "SELECT " + weather_attributes_with_id + " FROM WEATHER"
weather_clear = "DELETE FROM WEATHER"

### SUBJECT_GROUP QUERIES########################################
subject_group_attributes = "TITLE, DESCRIPTION"
subject_group_attributes_with_id = "SUBJECT_GROUP_ID, " + subject_group_attributes
subject_group_insert = "INSERT INTO SUBJECT_GROUP(" + subject_group_attributes + ") values (:1, :2)"
subject_group_select_all = "SELECT " + subject_group_attributes_with_id + " FROM SUBJECT_GROUP"
subject_group_clear = "DELETE FROM SUBJECT_GROUP"

### DIGITALISATION QUERIES####################################
digitization_attributes = "GAIN, FILTER, SAMPLING_RATE"
digitization_attributes_with_id = "DIGITIZATION_ID, " + digitization_attributes
digitization_insert = "INSERT INTO DIGITIZATION(" + digitization_attributes + ") VALUES(:1, :2, :3)"
digitization_select_all = "SELECT " + digitization_attributes_with_id + " FROM DIGITIZATION"
digitization_clear = "DELETE FROM DIGITIZATION"

### SUBJECT_GROUP QUERIES########################################
electrode_system_attributes = "TITLE, DESCRIPTION"
electrode_system_attributes_with_id = "electrode_system_ID, " + electrode_system_attributes
electrode_system_insert = "INSERT INTO electrode_system(" + electrode_system_attributes + ") values (:1, :2)"
electrode_system_select_all = "SELECT " + electrode_system_attributes_with_id + " FROM electrode_system"
electrode_system_clear = "DELETE FROM electrode_system"


### COMPOSITE FUNCTIONS#######################################
def clear_db():
    clear_scenarios()
    clear_groups()
    clear_persons()
    clear_artefacts()
    clear_weathers()
    clear_subject_groups()
    clear_digitizations()
    clear_electrode_systems()

### GENERIC FUNCTIONS#########################################
def connect():
    con = cx_Oracle.connect('DB2/db@127.0.0.1/DB')
    return con

def insert_many(query, params=[]):
    con = connect()
    cur = con.cursor()
    cur.bindarraysize = len(params)

    cur.prepare(query)
    cur.executemany(None, params)
    con.commit()

    cur.close()
    con.close()

def update(query, params=[]):
    con = connect()
    cur = con.cursor()
    cur.bindarraysize = len(params)

    cur.prepare(query)
    cur.execute(None, params)
    con.commit()

    cur.close()
    con.close()

def fetch_many(query, params=[]):
    con = connect()
    cur = con.cursor()

    cur.prepare(query)
    cur.execute(None, params)
    res = cur.fetchall()

    cur.close()
    con.close()

    return res

def fetch_one(query, params=[]):
    con = connect()
    cur = con.cursor()

    cur.prepare(query)
    cur.execute(None, params)
    res = cur.fetchone()

    cur.close()
    con.close()

    return res

### PERSON FUNCTIONS##########################################
def save_persons(persons=[]):
    insert_many(person_insert, ut.persons_to_matrix(persons))

def query_persons(query, parameters=[]):
    persons = []
    for t in fetch_many(query, parameters):
        persons.append(person(t[1], t[2], t[3], t[4], t[0]))

    return persons

def query_person(query, parameters=[]):
    t = fetch_one(query, parameters)
    return  person(t[1], t[2], t[3], t[4], t[0])

def clear_persons():
    update(person_clear)

### RESEARCH GROUP FUNCTIONS###################################

def save_research_groups(groups=[]):
    insert_many(research_group_insert, ut.groups_to_matrix(groups))

def add_res_group_members(group, persons=[]):
    insert_many(research_group_member_insert, ut.prepare_member_matrix(group, persons))

def query_groups(query, parameters=[]):
    groups = []
    for t in fetch_many(query, parameters):
        owner = query_person(person_select_by_id, [t[3]])
        groups.append(research_group(owner, t[1], t[2], t[0]))

    return groups

def query_group(query, parameters=[]):
    t = fetch_one(query, parameters)
    owner = query_person(person_select_by_id, [t[3]])
    return research_group(owner, t[1], t[2], t[0])

def clear_groups():
    update(research_group_member_clear)
    update(research_group_clear)

### SCENARIO FUNCTIONS########################################
def save_scenarios(scenarios=[]):
    insert_many(scenario_insert, ut.scenarios_to_matrix(scenarios))

def query_scenarios(query, parameters=[]):
    scenarios = []
    for s in fetch_many(query, parameters):
        owner = query_person(person_select_by_id, s[3])
        group = query_group(research_group_select_by_id, s[4])
        scenarios.append(scenario(owner, group, s[1], s[2], s[0]))

    return scenarios

def query_scenario(query, parameters=[]):
    s = fetch_one(query, parameters)
    owner = query_person(person_select_by_id, s[3])
    group = query_group(research_group_select_by_id, s[4])
    return scenario(owner, group, s[1], s[2], s[0])

def clear_scenarios():
    update(scenario_clear)

### ARTEFACT FUNCTIONS########################################
def save_artefacts(artefacts=[]):
    insert_many(artefact_insert, ut.artefacts_to_matrix(artefacts))

def query_artefacts(query, parameters=[]):
    artefacts = []
    for t in fetch_many(query, parameters):
        artefacts.append(artefact(t[1], t[2], t[0]))

    return artefacts

def query_artefact(query, parameters=[]):
    t = fetch_one(query, parameters)
    return artefact(t[1], t[2], t[0])

def clear_artefacts():
    update(artefact_clear)

### WEATHER FUNCTIONS#########################################
def save_weather(weather=[]):
    insert_many(weather_insert, ut.weather_to_matrix(weather))

def query_weathers(query, parameters=[]):
    weathers = []
    for t in fetch_many(query, parameters):
        weathers.append(weather(t[1], t[2], t[0]))

    return weathers

def query_weather(query, parameters=[]):
    t = fetch_one(query, parameters)
    return weather(t[1], t[2], t[0])

def clear_weathers():
    update(weather_clear)

### SUBJECT GROUP FUNCTIONS####################################
def save_subject_group(subject_group=[]):
    insert_many(subject_group_insert, ut.subject_group_to_matrix(subject_group))

def query_subject_groups(query, parameters=[]):
    subject_groups = []
    for t in fetch_many(query, parameters):
        subject_groups.append(subject_group(t[1], t[2], t[0]))

    return subject_groups

def query_subject_group(query, parameters=[]):
    t = fetch_one(query, parameters)
    return subject_group(t[1], t[2], t[0])

def clear_subject_groups():
    update(subject_group_clear)

### DIGITALISATION FUNCTIONS##################################
def save_digitalization(digit = []):
    insert_many(digitization_insert, ut.digitization_to_matrix(digit))

def query_digitizations(query, parameters=[]):
    digits = []
    for t in fetch_many(query, parameters):
        digits.append(digitization(t[1], t[2], t[3], t[0]))

    return digits

def query_digitization(query, paramters=[]):
    t = fetch_one(query, paramters)
    return digitization(t[1], t[2], t[3], t[0])

def clear_digitizations():
    update(digitization_clear)

### ELECTRODE SYSTEM FUNCTIONS####################################
def save_electrode_system(electrode_system=[]):
    insert_many(electrode_system_insert, ut.electrode_system_to_matrix(electrode_system))

def query_electrode_systems(query, parameters=[]):
    electrode_systems = []
    for t in fetch_many(query, parameters):
        electrode_systems.append(electrode_system(t[1], t[2], t[0]))

    return electrode_systems

def query_electrode_system(query, parameters=[]):
    t = fetch_one(query, parameters)
    return electrode_system(t[1], t[2], t[0])

def clear_electrode_systems():
    update(electrode_system_clear)