__author__ = 'veveri'

from datetime import datetime

class experiment:

    def __init__(self):
        self.id = 0
        self.start_time = datetime(2012, 12, 12, 13, 22)
        self.end_time = datetime(2012, 12, 12, 13, 42)
        self.owner = person()
        self.research_group = research_group()
        self.scenario = scenario()
        self.artefact = artefact()
        self.subject = person()
        self.temperature = 0
        self.environment_note = ""
        return


class person:

    def __init__(self, firstname="", lastname="", gender="M", laterality='X', id=0):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.laterality = laterality
        self.education_level_id = 1



class research_group:

    def __init__(self, owner, title="", desc="", id=0):
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
    def __init__(self, title="", desc="", id=0):
        self.id = id
        self.title = title
        self.desc = desc

    def __str__(self):
        return "Electrode system: " + self.title + ", desc: " + self.desc