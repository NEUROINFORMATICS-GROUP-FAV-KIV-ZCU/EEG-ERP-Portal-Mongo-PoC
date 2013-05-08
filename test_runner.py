__author__ = 'veveri'

from data.classes import *
import data.generator as gen
import oracle as oc


#oc.save_persons(gen.generate_persons(1, 10))
#owners = oc.query_persons(oc.person_select_all)

#oc.save_research_groups(gen.generate_research_groups(5, owners))

#groups = oc.query_groups(oc.research_group_select_all)
#scenarios = gen.generate_scenarios(10, groups)
#oc.save_scenarios(scenarios)
#oc.clear_db()

print "### STARTING TEST RUN ###"
#gen.init_oracle(100, 100, 100, 10, 100, 100, 200, 100, 100)
gen.generate_experiments()
print "### TEST RUN FINISHED ###"




