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

def prepare_member_matrix(group, persons=[]):
    ret = []
    for p in persons:
        ret.append(prepare_member_tuple(group, p))

    return ret

def prepare_member_tuple(group, p):
    return str(p.id), str(group.id), "GROUP_ADMIN"

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

def weather_to_matrix(weather=[]):
    ret = []
    for w in weather:
        ret.append(weather_to_tuple(w))

    return ret

def weather_to_tuple(w):
    return str(w.title), str(w.desc)

def subject_group_to_matrix(s_group=[]):
    ret = []
    for w in s_group:
        ret.append(subject_group_to_tuple(w))

    return ret

def subject_group_to_tuple(w):
    return str(w.title), str(w.desc)

def digitization_to_matrix(digits=[]):
    ret = []
    for d in digits:
        ret.append(digitization_to_tuple(d))

    return ret

def digitization_to_tuple(d):
    return str(d.gain), str(d.filter), str(d.sampling_rate)