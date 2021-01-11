import re

class FormsEbApp():

    def generateSelectChoices(self, query_result, query_result_columnname, empty_firstline=True):

        splited_query_results = query_result[query_result_columnname].split("\r\n")

        choices = []
        
        if empty_firstline is True:
            choices.append(('', ''))  

        for single_result in splited_query_results:
            choices.append((single_result, single_result))

        return choices

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