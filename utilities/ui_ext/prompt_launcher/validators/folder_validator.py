import os

from utilities.ui_ext.prompt_launcher.validators.validator import Validator


class ValidateFolderExistence(Validator):
    def validate(self, input=None):
        """Check given directory for existence
        Returns
        -------
        input : any
        """
        if os.path.exists(input):
            return input

        return None
