import logging

from azuresearch.skills import Skill, SkillInput, SkillOutput

predefined_skills = {
    "KeyPhraseExtractionSkill": "#Microsoft.Skills.Text.KeyPhraseExtractionSkill",
    "LanguageDetectionSkill": "#Microsoft.Skills.Text.LanguageDetectionSkill",
    "EntithRecognitionSkill": "#Microsoft.Skills.Text.EntityRecognitionSkill",
    "MergeSkill": "Microsoft.Skills.Text.MergeSkill",
    "SplitSkill": "Microsoft.Skills.Text.SplitSkill",
    "SentimentSkill": "Microsoft.Skills.Text.SentimentSkill",
    "ImageAnalysisSkill": "Microsoft.Skills.Vision.ImageAnalysisSkill",
    "OCRSkill": "#Microsoft.Skills.Vision.OcrSkill",
    "ShaperSkill": "Microsoft.Skills.Util.ShaperSkill"
}


class KeyPhraseExtractionSkill(Skill):
    """
    The Key Phrase Extraction skill evaluates unstructured text, and for each record, returns a list of key phrases.
    This capability is useful if you need to quickly identify the main talking points in the record. For example, given input text "The food was delicious and there were wonderful staff", the service returns "food" and "wonderful staff".

    :param default_language_code: The language code to apply to documents that don't specify language explicitly. If the default language code is not specified, English (en) will be used as the default language code.
    See Full list of supported languages.
    :param max_key_phrase_count: The maximum number of key phrases to produce.
    """

    def __init__(self, inputs=None, outputs=None, context="/document/pages/*", default_language_code='en',
                 max_key_phrase_count=30):
        if inputs is None:
            inputs = self.get_default_inputs()

        if outputs is None:
            outputs = self.get_default_outputs()

        params = {"defaultLanguageCode": default_language_code,
                  "maxKeyPhraseCount": max_key_phrase_count}

        super(KeyPhraseExtractionSkill, self).__init__(skill_type=
                                                       predefined_skills['KeyPhraseExtractionSkill'], inputs=inputs,
                                                       outputs=outputs, context=context, **params)

    def get_default_outputs(self):
        logging.debug("Using default outputs")
        outputs = [SkillOutput("keyPhrases", "keyPhrases")]
        return outputs

    def get_default_inputs(self):
        logging.debug("Using default inputs")

        inputs = [SkillInput("text", "/document/text"),
                  SkillInput("languageCode", "/document/languageCode")
                  ]
        return inputs


class LanguageDetectionSkill(Skill):
    """
    For up to 120 languages, the Language Detection skill detects the language of input text and reports
    a single language code for every document submitted on the request.
    The language code is paired with a score indicating the strength of the analysis.
    This capability is especially useful when you need to provide the language of the text as input to other skills
    (for example, the Sentiment Analysis skill or Text Split skill).
    """

    def __init__(self, categories, inputs, outputs, context):
        super(LanguageDetectionSkill, self).__init__(skills=predefined_skills['LanguageDetectionSkill'],
                                                     categories=categories, inputs=inputs, outputs=outputs,
                                                     context=context)


class MergeSkill(Skill):
    """
    :param insert_pre_tag: String to be included before every insertion.
    The default value is " ". To omit the space, set the value to "".
    :param insert_post_tag: String to be included after every insertion.
    The default value is " ". To omit the space, set the value to "".
     """

    def __init__(self, inputs, outputs, context, insert_pre_tag=" ", insert_post_tag=" ", ):
        params = {"insertPreTag": insert_pre_tag,
                  "insertPostTag": insert_post_tag}

        super(MergeSkill, self).__init__(skill_type=predefined_skills['MergeSkill'], inputs=inputs, outputs=outputs, context=context, **params)


class SplitSkill(Skill):
    """
    he Text Split skill breaks text into chunks of text.
    You can specify whether you want to break the text into sentences or into pages of a particular length.
    This skill is especially useful if there are maximum text length requirements in other skills downstream.
    :param text_split_mode: 	Either "pages" or "sentences"
    :param maximum_page_length: 	If textSplitMode is set to "pages", this refers to the maximum page length as measured by String.Length. The minimum value is 100. If the textSplitMode is set to "pages", the algorithm will try to split the text into chunks that are at most "maximumPageLenth" in size. In this case, the algorithm will do its best to break the sentence on a sentence boundary, so the size of the chunk may be slightly less than "maximumPageLength".
    :param default_language_code: 	(optional) One of the following language codes: da, de, en, es, fi, fr, it, ko, pt. Default is English (en). Few things to consider:

    If you pass a languagecode-countrycode format, only the languagecode part of the format is used.
    If the language is not in the previous list, the split skill breaks the text at character boundaries.
    Providing a language code is useful to avoid cutting a word in half for non-space languages such as Chinese, Japanese, and Korean.
    """

    def __init__(self, categories, inputs, outputs, context, text_split_mode='pages', maximum_page_length=None,
                 default_language_code='en'):
        params = {"testSplitMode": text_split_mode,
                  "maximumPageLength": maximum_page_length,
                  "defaultLanguageCode": default_language_code}

        super(SplitSkill, self).__init__(predefined_skills['SplitSkill'], categories, inputs,
                                         outputs, context,**params)
