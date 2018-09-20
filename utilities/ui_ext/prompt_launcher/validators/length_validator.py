from utilities.ui_ext.prompt_launcher.validators.validator import Validator


class LengthValidator(Validator):
    def __init__(self, minL=0, maxL=0):
        self.minL = minL
        self.maxL = maxL

    def validate(self, input=None):
        """Check input length.
        Parameters
        -------
        minL | integer
        maxL | integer
        Returns
        -------
        input : any
        """
        if len(input) >= self.minL and len(input) <= self.maxL:
            return input

        return None
