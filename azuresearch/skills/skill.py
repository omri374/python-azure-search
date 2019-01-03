import json


class Skill(object):
    def __init__(self, skill_type, inputs, outputs, context, **params):
        """

        :param skill_type: the type of skill (@odata.type)
        :param inputs: A list of objects of type SkillInput which represent the desire inputs for this skill
        :param outputs: A list of objects of type SkillOutput which represent the desired outputs for this skill
        :param context: Each skill should have a "context". The context represents the level at which operations take place
        :param params: Additional arguments for this skill
        """

        if (inputs is None) or (len(inputs) == 0):
            raise Exception("Inputs must be provided")
        if not isinstance(inputs[0], SkillInput):
            raise TypeError("Inputs should be of type SkillInput")
        if (outputs is None) or (len(outputs) == 0):
            raise Exception("outputs must be provided")
        if not isinstance(outputs[0], SkillOutput):
            raise TypeError("Outputs should be of type SkillOutput")

        self.skill_type = skill_type
        self.inputs = inputs
        self.outputs = outputs
        self.context = context
        if params:
            self.params = params['kwargs']
        else:
            self.params = {}

    def to_dict(self):
        dict = {
            "@odata.type": self.skill_type,
            "inputs": [inp.to_dict() for inp in self.inputs],
            "outputs": [outp.to_dict() for outp in self.outputs],
            "context": self.context
        }

        #Add additional arguments
        dict.update(self.params)

        #Remove None values
        dict = {k: v for k, v in dict.items() if v is not None}
        return dict

    @classmethod
    def load(cls, data, **kwargs):
        if data:
            if type(data) is str:
                data = json.loads(data)
            if type(data) is not dict:
                raise Exception("Failed to load JSON file with skill data")
            kwargs.update(data)
            if "@odata.type" not in data:
                raise Exception("Please provide the skill type (@odata.type)")
            if "inputs" not in data:
                raise Exception("Please provide the skill inputs")
            if "outputs" not in data:
                raise Exception("Please provide the skill outputs")

            if 'context' not in data:
                data['context'] = None

            return cls(data['@odata.type'], data['inputs'], data['outputs'], data['context'], **kwargs)
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


class SkillOutput(object):
    """
    Defines the output of a skill
    """

    def __init__(self, name, targetName):
        self.name = name
        self.targetName = targetName

    def to_dict(self):
        return {
            "name": self.name,
            "targetName": self.targetName
        }
