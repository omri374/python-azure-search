import json

from azuresearch.azure_search_object import AzureSearchObject


class Skill(AzureSearchObject):
    def __init__(self, **kwargs):
        """

        :param skill_type: the type of skill (@odata.type)
        :param inputs: A list of objects of type SkillInput which represent the desire inputs for this skill
        :param outputs: A list of objects of type SkillOutput which represent the desired outputs for this skill
        :param context: Each skill should have a "context". The context represents the level at which operations take place
        :param params: Additional arguments for this skill
        """

        if "inputs" not in kwargs:
            raise Exception("Inputs must be provided")
        inputs = kwargs['inputs']
        if not isinstance(inputs[0], SkillInput):
            raise TypeError("Inputs should be of type SkillInput")
        if "outputs" not in kwargs:
            raise Exception("outputs must be provided")
        outputs = kwargs['outputs']
        if not isinstance(outputs[0], SkillOutput):
            raise TypeError("Outputs should be of type SkillOutput")

        self.skill_type = kwargs.get("@odata.type")
        self.inputs = inputs
        self.outputs = outputs
        self.context = kwargs.get("context")

        self.params = {k:v for (k,v) in kwargs.items() if k not in ['@odata.type','inputs','outputs','context']}


    def to_dict(self):
        dict = {
            "@odata.type": self.skill_type,
            "inputs": [inp.to_dict() for inp in self.inputs],
            "outputs": [outp.to_dict() for outp in self.outputs],
            "context": self.context
        }

        # Add additional arguments
        dict.update(self.params)

        # Remove None values
        dict = Skill.remove_empty_values(dict)
        return dict

    @classmethod
    def load(cls, data):
        if data:
            if type(data) is str:
                data = json.loads(data)
            if type(data) is not dict:
                raise Exception("Failed to load JSON file with skill data")
            if "@odata.type" not in data:
                raise Exception("Please provide the skill type (@odata.type)")
            if "inputs" not in data:
                raise Exception("Please provide the skill inputs")
            if "outputs" not in data:
                raise Exception("Please provide the skill outputs")

            data['outputs'] = [SkillOutput.load(so) for so in data['outputs']]
            data['inputs'] = [SkillInput.load(so) for so in data['inputs']]

            if 'context' not in data:
                data['context'] = None
            skill_type = data['@odata.type']
            return cls(**data)
        else:
            raise Exception("data is null")


class SkillInput(object):
    """
    Defines an input for a skill
    """

    def __init__(self, name, source):
        self.name = name
        self.source = source

    def to_dict(self):
        return {
            "name": self.name,
            "source": self.source
        }

    @classmethod
    def load(cls, data):
        if data:
            if type(data) is str:
                data = json.loads(data)
            if type(data) is not dict:
                raise Exception("Failed to load JSON file with skill data")
            return cls(name=data['name'], source=data['source'])


class SkillOutput(object):
    """
    Defines the output of a skill
    """

    def __init__(self, name, target_name):
        self.name = name
        self.target_name = target_name

    def to_dict(self):
        return {
            "name": self.name,
            "targetName": self.target_name
        }

    @classmethod
    def load(cls, data):
        if data:
            if type(data) is str:
                data = json.loads(data)
            if type(data) is not dict:
                raise Exception("Failed to load JSON file with skill data")
            return cls(name=data['name'], target_name=data['targetName'])
