__author__ = 'Jakub Danek'

from data.classes import *

def persons_to_matrix(persons=[]):
    ret = []
    for p in persons:
        ret.append(person_to_touple(p))

    return ret

def person_to_touple(p):
    return str(p.firstname), str(p.lastname), str(p.gender), str(p.laterality), str(p.education_level_id)

def groups_to_matrix(groups):
    ret = []
    for g in groups:
        ret.append(res_group_to_touple(g))

    return ret

def res_group_to_touple(rg):
    return str(rg.title), str(rg.desc), int(rg.owner.id)

def data_to_json ():
    return