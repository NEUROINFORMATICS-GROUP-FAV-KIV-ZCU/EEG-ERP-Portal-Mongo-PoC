__author__ = 'Jakub Danek'

import cx_Oracle
import utils as ut
from data.classes import *
import data.generator as gen

### PERSON QUERIES##########################################
person_attributes = "GIVENNAME, SURNAME, GENDER, LATERALITY, EDUCATION_LEVEL_ID"
person_attributes_with_id = "PERSON_ID, " + person_attributes
person_insert = 'INSERT INTO PERSON(' + person_attributes + ') values(:1, :2, :3, :4, :5)'
person_select_all = "SELECT "  + person_attributes_with_id + " FROM PERSON"
person_select_by_id = person_select_all + " WHERE PERSON_ID = :1"

### RESEARCH GROUP QUERIES#################################
research_group_attributes = "TITLE, DESCRIPTION, OWNER_ID"
research_group_attributes_with_id = "RESEARCH_GROUP_ID, " + research_group_attributes
research_group_insert = "INSERT INTO RESEARCH_GROUP(" + research_group_attributes +") VALUES(:1, :2, :3)"
research_group_select_all = "SELECT " + research_group_attributes_with_id + " FROM RESEARCH_GROUP"

### GENERIC METHODS#########################################
def connect():
    con = cx_Oracle.connect('DB2/db@127.0.0.1/DB')
    return con

def insert(query, params=[]):
    con = connect()
    cur = con.cursor()
    cur.bindarraysize = len(params)

    cur.prepare(query)
    cur.executemany(None, params)
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


### PERSON METHODS##########################################
def save_persons(persons=[]):
    insert(person_insert, ut.persons_to_matrix(persons))

def query_persons(query, parameters=[]):
    persons = []
    for t in fetch_many(query, parameters):
        persons.append(person(t[1], t[2], t[3], t[4], t[0]))

    return persons

def query_person(query, parameters=[]):
    t = fetch_one(query, parameters)
    return  person(t[1], t[2], t[3], t[4], t[0])

### RESEARCH GROUP METHODS###################################

def save_research_groups(groups=[]):
    insert(research_group_insert, ut.groups_to_matrix(groups))

def query_groups(query, parameters=[]):
    groups = []
    for t in fetch_many(query, parameters):
        owner = query_person(person_select_by_id, [t[3]])
        groups.append(research_group(owner, t[1], t[2], t[0]))

    return groups
