import click

from utilities import Colors


class PromptLauncher:
    """Collect and execute prompt objects.
    """
    def __init__(self, prompts=[]):
        """Constructs the PromptLauncher object.
        Paramenters
        -------
        prompts | Prompt

        click | Click ( lib for python CLI )

        Returns
        -------
        None
        """
        self._prompts = prompts

    def add(self, propmts):
        """Add new items to dict with concat
        Returns
        -------
        None
        """

        self._prompts = self._prompts + propmts

    def pop_prompt(self):
        """Pop the first element from the prompts list.
        Returns
        -------
        prompt | Prompt
            prompt value
        """
        return self._prompts.pop(0)

    def recuresive_prompt(self, prompt, valuedict):
        return self.prompt(prompt, valuedict)

    def prompt(self, prompt, valuedict={}):
        """Execute given prompt object.
        Returns
        -------
        valuedict | Dictionary
            valuedict value
        """

        if prompt.validator:
            value = None

            err_msg = prompt.error_message
            fail_clr = Colors['FAIL'].value
            reset_clr = Colors['ENDC'].value

            if type(prompt.validator) is list:
                userInput = click.prompt(
                    prompt._message,
                    type=prompt.type,
                    default=prompt.default
                )

                for validator in prompt.validator:
                    validator_return = validator.validate(userInput)

                    if validator_return is None:
                        print(Colors['FAIL'].value + err_msg + reset_clr)
                        return self.recuresive_prompt(prompt, valuedict)

                    value = validator_return
            else:
                value = prompt.validator.validate(input=click.prompt(
                                                  prompt._message,
                                                  type=prompt.type,
                                                  default=prompt.default))
            if value is not None:
                valuedict[prompt.name] = value
            else:
                print(fail_clr + err_msg + reset_clr)
                return self.recuresive_prompt(prompt, valuedict)
        else:
            valuedict[prompt.name] = click.prompt(
                prompt._message,
                type=prompt.type,
                default=prompt.default,
            )

        return valuedict

    def multi_prompt(self):
        """Prompt the user with questions.
        Returns
        -------
        thisdict | Dictionary
            thisdict value
        """
        thisdict = {}

        while len(self._prompts) > 0:
            prompt = self._prompts.pop(0)
            thisdict = self.prompt(prompt, thisdict)
        return thisdict
