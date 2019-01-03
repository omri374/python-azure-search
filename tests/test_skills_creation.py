import pytest

from azuresearch.skills import Skillset, SkillInput, Skill, SkillOutput
from azuresearch.skills.predefined.cognitive_skills import KeyPhraseExtractionSkill
from tests.test_index_creation import get_json_file


def ordered(obj):
    """
    Order dictionary by keys, recursively
    :param obj:
    :return:
    """
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def get_simple_skill(type="my_skill_type", input_name="name", input_source="source", output_name="name",
                     output_target="target", context="context"):
    skill = Skill(type, [SkillInput(input_name, input_source)], [SkillOutput(output_name, output_target)], context=context)
    return skill


def test_skill_creation():
    skill = get_simple_skill()
    assert skill.inputs[0].name == "name"
    assert skill.inputs[0].source == "source"
    assert skill.outputs[0].name == "name"
    assert skill.outputs[0].targetName == "target"
    assert skill.skill_type == "my_skill_type"


def test_skill_to_dict():
    skill = get_simple_skill()
    assert skill.context == "context"
    assert skill.to_dict()['inputs'][0]['name'] == "name"
    assert skill.to_dict()['inputs'][0]['source'] == "source"
    assert skill.to_dict()['outputs'][0]['name'] == "name"
    assert skill.to_dict()['outputs'][0]['targetName'] == "target"
    assert skill.to_dict()["@odata.type"] == "my_skill_type"


def test_keyphrase_extraction_skill_same_as_json():
    keyphraseExtractionSkill = KeyPhraseExtractionSkill()
    actual = keyphraseExtractionSkill.to_dict()
    expected = get_json_file("keyphrase-extraction-skill.json")

    assert ordered(actual) == ordered(expected)


#### Skillset tests ####


def test_skillset_creation_empty_skills_throws_exception():
    with pytest.raises(Exception):
        skillset = Skillset("myskillset", [])


def test_skillset_simple_skill_wrong_type_throws_exception():
    input = SkillInput("myskill", "source")
    with pytest.raises(Exception):
        skillset = Skillset("myskillset", [input])


def test_skillset_init_correct():
    skill = get_simple_skill()
    skillset = Skillset("my_skillset", [skill], description="desc")
    skillset.name = "my_skillset"
    skillset.description = "desc"
    skillset.skills = [skill]


def test_skillset_to_dict_correct():
    skill1 = get_simple_skill("type1")
    skill2 = get_simple_skill("type2")
    skill3 = get_simple_skill("type3")
    skillset = Skillset("my_skillset", [skill1, skill2, skill3], description="desc")
    dict = skillset.to_dict()
    assert dict['name'] == "my_skillset"
    assert dict['skills'][0]['@odata.type']=='type1'
    assert dict['skills'][1]['@odata.type']=='type2'
    assert dict['skills'][2]['@odata.type']=='type3'
