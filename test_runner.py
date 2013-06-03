__author__ = 'Jakub Danek'

"""
Test control module.
"""
from data.classes import *
import data.generator as gen
import oracle as oc
import mongo as m
import sys
import tests

"""
Run all test cases. Number of inrementation steps depends on the steps parameter.
Steps parameter represents maximum number of parallel processes (1 - 2^steps).
"""
def incremental_test(steps=1):
    scenario_title_incremental_test(steps)
    group_owner_name_incremental_test(steps)
    subject_age_incremental_test(steps)

"""
Search by subject age.
"""
def subject_age_incremental_test(steps=1):
    proc = 1
    print "### STARTING TEST RUN: SUBJECT AGE###"
    for i in range(0, steps):
        tests.search_experiments_by_subject_age(60,proc)
        proc = proc * 2
        print "ITERATION: " + str(i) + " PASSED"
    print "### TEST RUN - SUBJECT AGE - FINISHED ###"

"""
Search by scenario title
"""
def scenario_title_incremental_test(steps=1):
    proc = 1
    print "### STARTING TEST RUN: SCENARIO TITLE###"
    for i in range(0, steps):
        tests.search_experiments_by_scenario_name("scenario1", proc)
        proc = proc * 2
        print "ITERATION: " + str(i) + " PASSED"
    print "### TEST RUN - SCENARIO TITLE - FINISHED ###"

"""
Search by research group owner.
"""
def group_owner_name_incremental_test(steps=1):
    proc = 1
    print "### STARTING TEST RUN: GROUP OWNER NAME###"
    for i in range(0, steps):
        tests.search_experiments_by_research_group_owner_name("firstname9", "lastname2", proc)
        proc = proc * 2
        print "ITERATION: " + str(i) + " PASSED"
    print "### TEST RUN - GROUP OWNER NAME - FINISHED ###"


"""
Initializes both the databases.
"""
def init_dbs():
    gen.init_oracle(100, 100, 100, 10, 100, 100, 200, 100, 100)
    gen.generate_experiments()
    exps = oc.query_experiments_full(oc.experiment_select_full_all)
    m.init_mongo(exps)

if __name__ == "__main__":
    incremental_test(1)