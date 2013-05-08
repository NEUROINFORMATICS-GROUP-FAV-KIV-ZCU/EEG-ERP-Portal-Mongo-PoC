__author__ = 'veveri'

from datetime import datetime

class experiment:

    def __init__(self, owner=None, r_group=None, scenario=None, artefact=None, subject=None, electrode=None, digit=None, s_group=None, weather=None, id = 0):
        self.id = id
        self.start_time = datetime(2012, 12, 12, 13, 22)
        self.end_time = datetime(2012, 12, 12, 13, 42)
        self.owner = owner
        self.research_group = r_group
        self.scenario = scenario
        self.artefact = artefact
        self.subject = subject
        self.temperature = 0
        self.environment_note = ""
        self.electrode = electrode
        self.digitization = digit
        self.subject_group = s_group
        self.weather = weather

    def to_dict(self):
        return {
            "experiment_id": self.id,
            "header": self.make_header(),
            "scenario": self.make_scenario(),
            "subject": self.make_subject(),
            "configuration": self.make_configuration()
        }

    def make_configuration(self):
        return {
            "temperature": self.temperature,
            "weather": self.make_weather(),
            "environment_note": self.environment_note,
            "artefact": self.make_artefact(),
            "electrode_system": self.electrode.title,
            "digitization": self.make_digitization()
        }

    def make_digitization(self):
        return {
            "sampling_rate": self.digitization.sampling_rate,
            "gain": self.digitization.gain
        }

    def make_artefact(self):
        return {
            "compensation": self.artefact.compensation,
            "reject_condition": self.artefact.reject_condition
        }

    def make_weather(self):
        return {
            "title": self.weather.title,
            "description": self.weather.desc
        }

    def make_subject(self):
        subj = self.make_person(self.subject)
        subj["gender"] = self.subject.gender
        #subj["date_of_birth"] = self.subject.date_of_birth
        subj["laterality"] = self.subject.laterality
        subj["group"] = {}
        subj["group"]["title"] = self.subject_group.title
        subj["group"]["description"] = self.subject_group.desc
        return subj


    def make_scenario(self):
        return {
            "name": self.scenario.title,
            "description": self.scenario.description,
            "owner": self.make_person(self.scenario.owner)
        }

    def make_header(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "owner": self.make_person(self.owner),
            "research_group": self.make_r_group()
        }

    def make_r_group(self):
        return {
            "title": self.research_group.title,
            "owner": self.make_person(self.research_group.owner)
        }

    def make_person(self, person):
        return {
            "firstname": person.firstname,
            "lastname": person.lastname
        }



class person:

    def __init__(self, firstname="", lastname="", gender="M", laterality='X', id=0):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.laterality = laterality
        self.education_level_id = 1



class research_group:

    def __init__(self, owner= person(), title="", desc="", id=0):
        self.id = id
        self.owner = owner
        self.title = title
        self.desc = desc

    def __str__(self):
        return "ResearchGRoup: " + self.title + ", Desc: " + self. desc


class scenario:
    def __init__(self, owner, group, title="", desc="", id=0):
        self.id = id;
        self.title = title
        self.description = desc
        self.owner = owner
        self.group = group

    def __str__(self):
        return "Scenario: " + self.title + ", desc: " + self.description + ", owner: " + self.owner

class artefact:
    def __init__(self, compensation="", reject_condition="", id=0):
        self.id = id
        self.compensation = compensation
        self.reject_condition = reject_condition

    def __str__(self):
        return "Artefact: " + self.compensation + ", reject condition: " + self.reject_condition

class weather:
    def __init__(self, title="", desc="", id=0):
        self.id = id
        self.title = title
        self.desc = desc

    def __str__(self):
        return "Weather: " + self.title + ", desc: " + self.desc

class subject_group:
    def __init__(self, title="", desc="", id=0):
        self.id = id
        self.title = title
        self.desc = desc

    def __str__(self):
        return "Subject group: " + self.title + ", desc: " + self.desc

class digitization:
    def __init__(self, gain=0.0, filter="", sampling=0.0, id=0):
        self.id = id
        self.gain = gain
        self.filter=filter
        self.sampling_rate=sampling

    def __str__(self):
        return "Digitization: " + self.filter + ", values: " + self.gain + ", " + self.sampling_rate

class electrode_system:
    def __init__(self, title="", desc="", id=0, conf_id=0):
        self.id = id
        self.conf_id=conf_id
        self.title = title
        self.desc = desc

    def __str__(self):
        return "Electrode system: " + self.title + ", desc: " + self.desc