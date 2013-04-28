__author__ = 'Jakub Danek'

from data.classes import *

def persons_to_matrix(persons=[]):
    ret = []
    for p in persons:
        ret.append(person_to_tuple(p))

    return ret

def person_to_tuple(p):
    return str(p.firstname), str(p.lastname), str(p.gender), str(p.laterality), str(p.education_level_id)

def groups_to_matrix(groups):
    ret = []
    for g in groups:
        ret.append(res_group_to_tuple(g))

    return ret

def res_group_to_tuple(rg):
    return str(rg.title), str(rg.desc), int(rg.owner.id)

def scenarios_to_matrix(scenarios=[]):
    ret = []
    for s in scenarios:
        ret.append(scenario_to_tuple(s))

    return ret

def scenario_to_tuple(s):
    return str(s.title), str(s.description), str(s.owner.id), str(s.group.id)

def artefacts_to_matrix(artefacts=[]):
    ret = []
    for a in artefacts:
        ret.append(artefact_to_tuple(a))

    return ret

def artefact_to_tuple(a):
    return str(a.compensation), str(a.reject_condition)