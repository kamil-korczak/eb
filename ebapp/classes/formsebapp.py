import re

class FormsEbApp():

    def generateSelectModelChoicesPlusEmpty(self, model_choices):

        choices = []
        choices.append(('', ''))

        for single_choice in model_choices:
            choices.append((single_choice[0], single_choice[1]))

        return choices

    def checkForExternalId(self, field):
        pattern = re.compile(r'[0-9]{12}')
        regex_result = pattern.search(field)
        
        if regex_result:
            data = regex_result.group(0)
        else:
            data = None

        return data