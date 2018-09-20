class Prompt:
    """Represent abstraction of python click
    propmt data.
    """
    def __init__(self, name, type, message=None, default=None, validator=None,
                 err_message=None):
        self.name = name
        self.type = type
        self.message = message
        self.default = default
        self.validator = validator
        self.error_message = err_message

    @property
    def name(self):
        """Getter for name property.
        Returns
        -------
        name : str
            name value
        """
        return self._name

    @name.setter
    def name(self, name):
        """Setter for name property.
        Parameters
        ----------
        name : str
            Defines the name value
        """

        if len(name) < 1:
            raise Exception("""The name property can not be
            with lenght less ten 1.""")

        self._name = name

    @property
    def type(self):
        """Getter for type property.
        Returns
        -------
        type | str
            type value
        """
        return self._type

    @type.setter
    def type(self, type):
        """Setter for type property.
        Parameters
        ----------
        type : str
            Defines the name value
        """

        self._type = type

    @property
    def message(self):
        """Getter for message property.
        Returns
        -------
        message | str
            message value
        """

        return self._message

    @message.setter
    def message(self, message=None):
        """Setter for message property.
        Parameters
        ----------
        message : str
            Defines the message value
        """

        if type(message) is not str:
            raise Exception("The message property has to be string")

        self._message = message

    @property
    def default(self):
        """Getter for default property.
        Returns
        -------
        default | any
            default value
        """

        return self._default

    @default.setter
    def default(self, default):
        """Setter for default property.
        Parameters
        ----------
        default : any
            Defines the message value
        """

        self._default = default

    @property
    def validator(self):
        """Getter for validator property.
        Returns
        -------
        validator | Validator / Validator[]
            validator value
        """

        return self._validator

    @validator.setter
    def validator(self, validator):
        """Setter for validator property.
        Parameters
        ----------
        validator : Validator | Validator[]
            Defines the validator value
        """

        self._validator = validator

    @property
    def error_message(self):
        """Getter for error_message property.
        Returns
        -------
        error_message | boolean
            error_message value
        """
        return self._error_message

    @error_message.setter
    def error_message(self, err_message):
        """Setter for error_message property.
        Parameters
        ----------
        error_message : boolean
            Defines the error_message value
        """

        if err_message is not None:
            self._error_message = err_message
