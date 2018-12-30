class Skill(object):
    def __init__(self, skill_type, categories, default_language_code, inputs, outputs, context,web_api_skill_uri=None):
        self.skill_type = skill_type
        self.categories = categories
        self.default_language_code = default_language_code
        self.context = context
        self.inputs = inputs
        self.outputs = outputs,


    def to_dict(self):
        return {
            "@odata.type": self.skill_type,
            "categories": self.categories,
            "context": self.context,
            "defaultLanguageCode": self.default_language_code,
            "inputs": [inp.to_dict() for inp in self.inputs],
            "outputs": [outp.to_dict() for outp in self.outputs]
        }


class SkillInput(object):
    def __init__(self, name, source):
        self.name = name
        self.source = source

    def to_dict(self):
        return {
            "name": self.name,
            "source": self.source
        }


class SkillOutput(object):
    def __init__(self, name, targetName):
        self.name = name
        self.targetName = targetName

    def to_dict(self):
        return {
            "name": self.name,
            "targetName": self.targetName
        }
