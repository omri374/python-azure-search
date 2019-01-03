import json

from azuresearch.skills import Skill

WEBAPP_SKILL = "#Microsoft.Skills.Custom.WebApiSkill"


class WebApiSkill(Skill):

    def __init__(self, inputs, outputs, context, **kwargs):
        super(WebApiSkill, self).__init__(skill_type=WEBAPP_SKILL, inputs=inputs, outputss=outputs, context=context, **kwargs)