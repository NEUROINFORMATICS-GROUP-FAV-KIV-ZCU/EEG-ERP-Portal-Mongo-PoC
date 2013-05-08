__author__ = 'Jakub Danek'

import cx_Oracle
import utils as ut
from data.classes import *

### PERSON QUERIES##########################################
person_attributes = "p.GIVENNAME, p.SURNAME, p.GENDER, p.LATERALITY, p.EDUCATION_LEVEL_ID"
person_attributes_with_id = "p.PERSON_ID, " + person_attributes
person_insert = 'INSERT INTO PERSON p(' + person_attributes + ') values(:1, :2, :3, :4, :5)'
person_select_all = "SELECT "  + person_attributes_with_id + " FROM PERSON p"
person_select_by_id = person_select_all + " WHERE p.PERSON_ID = :1"
person_select_by_lastname = person_select_all + " WHERE p.SURNAME = :1"
person_select_by_firstname = person_select_all + " WHERE p.GIVENNAME = :1"
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
research_group_member_select_by_group = person_select_all + ", RESEARCH_GROUP_MEMBERSHIP m WHERE p.PERSON_ID = m.PERSON_ID AND m.RESEARCH_GROUP_ID = :1"
research_group_member_clear = "DELETE FROM RESEARCH_GROUP_MEMBERSHIP"

### SCENARIO QUERIES#######################################
scenario_attributes = "TITLE, DESCRIPTION, OWNER_ID, RESEARCH_GROUP_ID"
scenario_attributes_with_id = "SCENARIO_ID, " + scenario_attributes
scenario_insert = "INSERT INTO SCENARIO(" + scenario_attributes + ") values (:1, :2, :3, :4)"
scenario_select_all = "SELECT " + scenario_attributes_with_id + " FROM SCENARIO"
scenario_select_all_full = "SELECT s.SCENARIO_ID, s.TITLE, s.DESCRIPTION, p.GIVENNAME, p.SURNAME, p.PERSON_ID FROM SCENARIO s, PERSON p WHERE s.OWNER_ID = p.PERSON_ID"
scenario_select_full_by_id = scenario_select_all_full + " AND SCENARIO_ID = :1"
scenario_select_by_id = scenario_select_all + " WHERE SCENARIO_ID = :1"
scenario_clear = "DELETE FROM SCENARIO"

### ARTEFACT QUERIES#######################################
artefact_attributes = "COMPENSATION, REJECT_CONDITION"
artefact_attributes_with_id = "ARTEFACT_ID, " + artefact_attributes
artefact_insert = "INSERT INTO ARTEFACT(" + artefact_attributes + ") VALUES (:1, :2)"
artefact_select_all = "SELECT " + artefact_attributes_with_id + " FROM ARTEFACT"
artefact_select_by_id = artefact_select_all + " WHERE ARTEFACT_ID = :1"
artefact_clear = "DELETE FROM ARTEFACT"

### WEATHER QUERIES########################################
weather_attributes = "TITLE, DESCRIPTION"
weather_attributes_with_id = "WEATHER_ID, " + weather_attributes
weather_insert = "INSERT INTO WEATHER(" + weather_attributes + ") values (:1, :2)"
weather_select_all = "SELECT " + weather_attributes_with_id + " FROM WEATHER"
weather_select_by_id = weather_select_all + " WHERE WEATHER_ID = :1"
weather_clear = "DELETE FROM WEATHER"

### SUBJECT_GROUP QUERIES########################################
subject_group_attributes = "TITLE, DESCRIPTION"
subject_group_attributes_with_id = "SUBJECT_GROUP_ID, " + subject_group_attributes
subject_group_insert = "INSERT INTO SUBJECT_GROUP(" + subject_group_attributes + ") values (:1, :2)"
subject_group_select_all = "SELECT " + subject_group_attributes_with_id + " FROM SUBJECT_GROUP"
subject_group_select_by_id = subject_group_select_all + " WHERE SUBJECT_GROUP_ID = :1"
subject_group_clear = "DELETE FROM SUBJECT_GROUP"

### DIGITALISATION QUERIES####################################
digitization_attributes = "GAIN, FILTER, SAMPLING_RATE"
digitization_attributes_with_id = "DIGITIZATION_ID, " + digitization_attributes
digitization_insert = "INSERT INTO DIGITIZATION(" + digitization_attributes + ") VALUES(:1, :2, :3)"
digitization_select_all = "SELECT " + digitization_attributes_with_id + " FROM DIGITIZATION"
digitization_select_by_id = digitization_select_all + " WHERE DIGITIZATION_ID = :1"
digitization_clear = "DELETE FROM DIGITIZATION"

### ELECTRODE CONF QUERIES########################################
electrode_system_attributes = "TITLE, DESCRIPTION"
electrode_system_attributes_with_id = "electrode_system_ID, " + electrode_system_attributes
electrode_system_insert = "INSERT INTO electrode_system(" + electrode_system_attributes + ") values (:1, :2)"
electrode_system_select_all = "SELECT " + electrode_system_attributes_with_id + " FROM electrode_system"
electrode_system_clear = "DELETE FROM electrode_system"
electrode_conf_insert = "INSERT INTO ELECTRODE_CONF (IMPEDANCE, ELECTRODE_SYSTEM_ID) VALUES(0, :1)"
electrode_conf_select_all = "SELECT c.ELECTRODE_CONF_ID, s.ELECTRODE_SYSTEM_ID, s.TITLE, s.DESCRIPTION FROM ELECTRODE_CONF c, ELECTRODE_SYSTEM s WHERE c.ELECTRODE_SYSTEM_ID = s.ELECTRODE_SYSTEM_ID"
electrode_conf_select_by_id = electrode_conf_select_all + " AND c.ELECTRODE_CONF_ID = :1"
electrode_system_clear = "DELETE FROM electrode_conf"

### EXPERIMENT QUERIES##########################################
experiment_attributes = "SCENARIO_ID, SUBJECT_PERSON_ID, WEATHER_ID, OWNER_ID, RESEARCH_GROUP_ID, ARTEFACT_ID, SUBJECT_GROUP_ID, ELECTRODE_CONF_ID, DIGITIZATION_ID"
experiment_attributes_with_id = "EXPERIMENT_ID, " +  experiment_attributes
experiment_insert = "INSERT INTO EXPERIMENT(" + experiment_attributes + ") VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)"
experiment_select_all = "SELECT " + experiment_attributes_with_id + " FROM EXPERIMENT"
experiment_clear = "DELETE FROM EXPERIMENT"
experiment_select_full_all = "SELECT e.EXPERIMENT_ID, e.SCENARIO_ID," \
                             " s.GIVENNAME, s.SURNAME, s.GENDER, s.LATERALITY," \
                             " w.TITLE, w.DESCRIPTION," \
                             " o.GIVENNAME, o.SURNAME, o.GENDER, o.LATERALITY," \
                             " e.RESEARCH_GROUP_ID," \
                             " a.COMPENSATION, a.REJECT_CONDITION," \
                             " sg.TITLE, sg.DESCRIPTION," \
                             " e.ELECTRODE_CONF_ID," \
                             " d.GAIN, d.FILTER, d.SAMPLING_RATE," \
                             " sc.TITLE, sc.DESCRIPTION, scp.GIVENNAME, scp.SURNAME," \
                             " rg.TITLE, rg.DESCRIPTION," \
                             " es.TITLE, es.DESCRIPTION" \
                             " FROM EXPERIMENT e, PERSON s, WEATHER w, PERSON o, ARTEFACT a, SUBJECT_GROUP sg, DIGITIZATION d, SCENARIO sc, PERSON scp," \
                             "      RESEARCH_GROUP rg, ELECTRODE_CONF ec, ELECTRODE_SYSTEM es" \
                             " WHERE e.SUBJECT_PERSON_ID = s.PERSON_ID" \
                             " AND e.WEATHER_ID = w.WEATHER_ID" \
                             " AND e.OWNER_ID = o.PERSON_ID" \
                             " AND e.ARTEFACT_ID = a.ARTEFACT_ID" \
                             " AND e.SUBJECT_GROUP_ID = sg.SUBJECT_GROUP_ID" \
                             " AND e.DIGITIZATION_ID = d.DIGITIZATION_ID" \
                             " AND e.SCENARIO_ID = sc.SCENARIO_ID" \
                             " AND sc.OWNER_ID = scp.PERSON_ID" \
                             " AND e.RESEARCH_GROUP_ID = rg.RESEARCH_GROUP_ID" \
                             " AND e.ELECTRODE_CONF_ID = ec.ELECTRODE_CONF_ID" \
                             " AND ec.ELECTRODE_SYSTEM_ID = es.ELECTRODE_SYSTEM_ID"


### COMPOSITE FUNCTIONS#######################################
def clear_db():
    clear_experients()
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

### EXPERIMENT FUNCTIONS######################################
def save_experiments(experiments=[]):
    insert_many(experiment_insert, ut.experiments_to_matrix(experiments))

#"EXPERIMENT_ID, SCENARIO_ID, SUBJECT_PERSON_ID, WEATHER_ID, OWNER_ID, RESEARCH_GROUP_ID, ARTEFACT_ID, SUBJECT_GROUP_ID, ELECTRODE_CONF_ID, DIGITIZATION_ID"
def query_experiments(query, parameters=[]):
    ret = []
    i = 0
    for t in fetch_many(query, parameters):

        subject = person(t[2], t[3], t[4], t[5])
        w = weather(t[6], t[7])
        owner = person(t[8], t[9], t[10], t[11])
        a = artefact(t[13], t[14])
        s_group = subject_group(t[15], t[16])
        digit = digitization(t[18], t[19], t[20])
        #scenario - research group is empty for now
        s = scenario(person(t[23], t[24]), research_group(), t[21], t[22], t[1])
        #research group - owner is empty for now
        r_group = research_group(person(), t[25], t[26], t[12])

        e = electrode_system(t[27], t[28])

        exp = experiment(owner, r_group, s, a, subject, e, digit, s_group, w)
        ret.append(exp)
        i += 1
        if(i % 1000 == 0):
            print(str(i) + " experiments loaded")


    return ret

def clear_experients():
    update(experiment_clear)

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
        owner = query_person(person_select_by_id, [s[3]])
        group = query_group(research_group_select_by_id, [s[4]])
        scenarios.append(scenario(owner, group, s[1], s[2], s[0]))

    return scenarios

#"s.SCENARIO_ID, s.TITLE, s.DESCRIPTION, p.GIVENNAME, p.SURNAME, p.PERSON_ID FROM SCENARIO s, PERSON p"
def query_scenarios_full(query, parameters=[]):
    scenarios = []
    for s in fetch_many(query, parameters):
        owner = person(s[3], s[4],'M','X', s[5])
        scenarios.append(scenario(owner, research_group(), s[1], s[2], s[0]))

    return scenarios

#"s.SCENARIO_ID, s.TITLE, s.DESCRIPTION, p.GIVENNAME, p.SURNAME, p.PERSON_ID FROM SCENARIO s, PERSON p"
def query_scenario_full(query, parameters=[]):
    s = fetch_one(query, parameters)
    owner = person(s[3], s[4],'M','X', s[5])
    return scenario(owner, research_group(), s[1], s[2], s[0])


def query_scenario(query, parameters=[]):
    s = fetch_one(query, parameters)
    owner = query_person(person_select_by_id, [s[3]])
    group = query_group(research_group_select_by_id, [s[4]])
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
    insert_many(electrode_conf_insert, ut.electrode_system_ids_to_matrix(query_electrode_systems(electrode_system_select_all)))

def query_electrode_systems(query, parameters=[]):
    electrode_systems = []
    for t in fetch_many(query, parameters):
        electrode_systems.append(electrode_system(t[1], t[2], t[0]))

    return electrode_systems

def query_electrode_system(query, parameters=[]):
    t = fetch_one(query, parameters)
    return electrode_system(t[1], t[2], t[0])

def query_electrode_confs(query, parameters=[]):
    electrode_confs = []
    for t in fetch_many(query, parameters):
        electrode_confs.append(electrode_system(t[2], t[3], t[1], t[0]))

    return electrode_confs

def query_electrode_conf(query, parameters=[]):
    t = fetch_one(query, parameters)
    return electrode_system(t[2], t[3], t[1], t[0])


def clear_electrode_systems():
    update(electrode_system_clear)