from abc import ABC, abstractstaticmethod
from utilities.ui_ext.prompt_launcher.validators import ValidateFolderExistence, LengthValidator, PatternValidator


class ValidatorFactory(ABC):
    @abstractstaticmethod
    def checkForFolderExistence():
        return ValidateFolderExistence()

    @abstractstaticmethod
    def pattern(pattern):
        return PatternValidator(pattern)

    @abstractstaticmethod
    def length(minL, maxL):
        return LengthValidator(minL=minL, maxL=maxL)