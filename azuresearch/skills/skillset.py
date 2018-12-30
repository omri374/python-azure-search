from azuresearch.service import Endpoint


class Skillset(object):
    endpoint = Endpoint("skillset")
    __name__ = "Skillset"

    def __init__(self, skillset_name, skills, skillset_desc=None):
        self.skillset_name = skillset_name
        self.skills = skills
        self.skillset_desc = skillset_desc
