__author__ = 'Jakub Daněk'

"""
This module contains various test cases and logic for results output.
"""

import oracle as oc
import mongo as mo
import timeit as t
from datetime import datetime
from threading import Thread
from threading import Lock

#TEST CASE QUERIES#####################################
_test_search_experiment_by_scenario_name_oracle="SELECT e.EXPERIMENT_ID FROM EXPERIMENT e, SCENARIO s" \
                                               " WHERE e.SCENARIO_ID = s.SCENARIO_ID" \
                                               " AND s.TITLE = :1"
_test_search_experiment_by_scenario_name_mongo={"scenario.name" : ""}

_test_search_experiment_by_research_group_owner_name_oracle="SELECT e.EXPERIMENT_ID FROM EXPERIMENT e, RESEARCH_GROUP r, PERSON p" \
                                                      " WHERE e.RESEARCH_GROUP_ID = r.RESEARCH_GROUP_ID" \
                                                      " AND r.OWNER_ID = p.PERSON_ID" \
                                                      " AND p.GIVENNAME = :1 AND p.SURNAME = :2"

_test_search_experiment_by_research_group_owner_name_mongo= {
                                                            "header.research_group.owner.firstname" : "",
                                                            "header.research_group.owner.lastname" : ""
                                                            }

_test_search_experiment_by_subject_age_oracle="SELECT e.EXPERIMENT_ID FROM EXPERIMENT e, PERSON p" \
                                       " WHERE e.SUBJECT_PERSON_ID = p.PERSON_ID" \
                                       " AND trunc((sysdate - p.DATE_OF_BIRTH) / 365.25) >= :1"
_test_search_experiment_by_subject_age_mongo={
    "subject.date_of_birth" : { "$lte" : "" }
}

#TEST CASE QUERIES#####################################

### GLOBAL VARIABLES###################################
_oracle_time = 0.0
_oracle_lock = Lock()
_mongo_time = 0.0
_mongo_lock = Lock()
### GLOBAL VARIABLES###################################

"""
Search by subject age.
age - minimum age of the subject
processes - number of parallel processes to run
check_integrity - test whether the returned datasets from both contain the same data
"""
def search_experiments_by_subject_age(age=18, processes=4, check_integrity=False):
    _init()

    #transform params into mongo search dictironary
    now = datetime.now()
    bday = datetime(now.year - age, now.month, now.day)
    _test_search_experiment_by_subject_age_mongo["subject.date_of_birth"]["$lte"]=bday

    ora_param = [age]
    #function references for integriy check and measure functions
    ora = lambda: oc.query_experiment_ids(_test_search_experiment_by_subject_age_oracle, ora_param)
    mon = lambda: mo.find_ids(_test_search_experiment_by_subject_age_mongo)
    #function references for paralel run
    ora_m = lambda: _measure_oracle(ora)
    mon_m = lambda: _measure_mongo(mon)
    #run the tests
    _paralel_run(processes,ora_m,mon_m)

    print "### SEARCH EXPERIMENTS BY SUBJECT AGE RESULTS ###"
    if(check_integrity):
        _check_integrity(ora, mon)
    print "Oracle: " + str(_oracle_time/processes)
    print "Mongo: " + str(_mongo_time/processes)
    print "########"


"""
Search by research group owner
processes - number of parallel processes to run
check_integrity - test whether the returned datasets from both contain the same data
"""
def search_experiments_by_research_group_owner_name(firstname="", lastname="", processes=4, check_integrity=False):
    _init()

    #transform params into mongo search dictironary
    _test_search_experiment_by_research_group_owner_name_mongo["header.research_group.owner.firstname"] = firstname
    _test_search_experiment_by_research_group_owner_name_mongo["header.research_group.owner.lastname"] = lastname

    ora_param = [firstname, lastname]
    #function references for integriy check and measure functions
    ora = lambda: oc.query_experiment_ids(_test_search_experiment_by_research_group_owner_name_oracle, ora_param)
    mon = lambda: mo.find_ids(_test_search_experiment_by_research_group_owner_name_mongo)
    #function references for paralel run
    ora_m = lambda: _measure_oracle(ora)
    mon_m = lambda: _measure_mongo(mon)
    #run the tests
    _paralel_run(processes,ora_m,mon_m)

    print "### SEARCH EXPERIMENTS BY RESEARCH GROUP OWNER RESULTS ###"
    if(check_integrity):
        _check_integrity(ora, mon)
    print "Oracle: " + str(_oracle_time/processes)
    print "Mongo: " + str(_mongo_time/processes)
    print "########"

"""
Search by scenario name
processes - number of parallel processes to run
check_integrity - test whether the returned datasets from both contain the same data
"""
def search_experiments_by_scenario_name(scenario_name, processes=4, check_integrity=False):
    _init()

    #transform params into mongo search dictironary
    _test_search_experiment_by_scenario_name_mongo["scenario.name"] = scenario_name

    #function references for integriy check and measure functions
    ora = lambda: oc.query_experiment_ids(_test_search_experiment_by_scenario_name_oracle, [scenario_name])
    mon = lambda: mo.find_ids(_test_search_experiment_by_scenario_name_mongo)
    #function references for paralel run
    ora_m = lambda: _measure_oracle(ora)
    mon_m = lambda: _measure_mongo(mon)
    #run the tests
    _paralel_run(processes,ora_m,mon_m)

    print "### SEARCH EXPERIMENTS BY SCENARIO TITLE RESULTS ###"
    if(check_integrity):
        _check_integrity(ora, mon)
    print "Oracle: " + str(_oracle_time/processes)
    print "Mongo: " + str(_mongo_time/processes)
    print "######"

"""
Restart tests module state.
"""
def _init():
    global _oracle_time
    global _oracle_lock
    global _mongo_time
    global _mongo_lock
    _oracle_time = 0.0
    _oracle_lock = Lock()
    _mongo_time = 0.0
    _mongo_lock = Lock()

"""
Measure time of run of an oracle query.
func - function to be run
num = number of repetitions
"""
def _measure_oracle(func, num=100):
    global _oracle_time

    i = t.timeit(func ,number=num)
    with _oracle_lock:
        _oracle_time += i

"""
Measure time of run of a mongo query.
func - function to be run
num = number of repetitions
"""
def _measure_mongo(func, num=100):
    global _mongo_time

    i = t.timeit(func ,number=num)
    with _mongo_lock:
        _mongo_time += i

"""
Runs each object in fns in parallel (n is number of processes).

Next functions is started only after all threads of the previous one stops.
"""
def _paralel_run(n=4,*fns):
    proc = []
    for f in fns:
        for i in range(0, n):
            p = Thread(target=f)
            proc.append(p)
        for p in proc:
            p.start()
        for p in proc:
            p.join()
        proc = []

"""
Check data integrity of the queries.

Only a dummy implementation (checks number of instances returned).
"""
def _check_integrity(ora_fun, mon_fun):
    ora_res = ora_fun()
    mon_res = mon_fun()
    ora_len = len(ora_res)
    mon_len = len(mon_res)
    if(ora_len == mon_len):
        print "Data integrity checked with no errors!"
    else :
        print "Test functions dont return same results!"
        print "Oracle length: " + str(ora_len)
        print "Mongo length: " + str(mon_len)