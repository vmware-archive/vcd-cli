import re

from utilities.ui_ext.prompt_launcher.validators.validator import Validator


class PatternValidator(Validator):
    def __init__(self, pattern):
        self.pattern = pattern

    def validate(self, input=None):
        """Check input structure agains given pattern.
        Returns
        -------
        input : any
        """
        if re.match(self.pattern, input):
            return input

        return None
