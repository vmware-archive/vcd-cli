import os
import queue
import json

from utilities.ui_ext.prompt_launcher import PromptLauncher, Prompt, ValidatorFactory
from utilities.ui_ext.cli_spinners import CliSpinner
from utilities.ui_ext.ext_generator import Generator
from pathlib import Path
from shutil import copyfile, rmtree


class ExtGenerator(Generator):
    def __init__(self):
        """Constructs the ExtGenerator object.
        Returns
        -------
        None
        """

    def parse_manifest(self):
        """Find manifest.json in the template path,
        read the file, parse it to dict and returns it.
        If no manifest file is found default dict will be
        returned.
        Returns
        -------
        manifest : dict
        """

        file = None

        try:
            file = Path(os.path.join(self.new_project_dir,
                                     'src/public/manifest.json'))
            raise Exception("blabal")
        except Exception:
            # Assign the file Path obj
            file = self.find_file(self.answers["template_path"],
                                  "manifest.json")

        # Check if file is found
        if file is not None:
            # Read the file
            with open(file, "r") as f:
                # Parse it to dict and returns it
                return json.loads(f.read())
        else:
            # Return default manifest values
            return {
                "urn": "vmware:vcloud:plugin:lifecycle",
                "name": "plugin-lifecycle",
                "containerVersion": "9.1.0",
                "version": "1.0.0",
                "scope": ["service-provider"],
                "permissions": [],
                "description": "",
                "vendor": "VMware",
                "license": "MIT",
                "link": "http://someurl.com",
                "module": "SubnavPluginModule",
                "route": "plugin-lifecycle"
            }

    def populate_manifest(self, basename, original_file_abs_path):
        """Open template file, read the file in-memory
        and populate the data given from user, creates
        the manifest.json with the new data.
        Returns
        -------
        None
        """
        # Read the original file
        readFile = open(original_file_abs_path, "r")

        # Create the new file and write the content
        with open(basename, "w") as f:
            # Parse the json content of the file
            files_json = json.loads(readFile.read())
            # Close the readable stream
            readFile.close()

            # Loop through answers
            for key, value in self.answers.items():
                # If answer key exist in the json
                if key in files_json:
                    # And if it is scope or permissions
                    if key == 'scope' or key == 'permissions':
                        # And if there is no content
                        if len(self.answers[key]) < 1:
                            # Assign empty array
                            value = []
                        else:
                            # If it's list already
                            if isinstance(self.answers[key], list):
                                value = self.answers[key]
                            else:
                                # Create array of strings
                                value = self.answers[key].split(", ")

                    # Assign the value to origin json file
                    files_json[key] = value

            # Write the new json to the newly created file with sorted keys
            # and 4 spaces indentation
            f.write(json.dumps(files_json, sort_keys=True, indent=4))
            # Close the writable stream
            f.close()

    def generate_files(self, entrie_full_abs_path, new_entrie_path, entrie):
        """Generate vCD UI Plugin files, manifest.json
        is populated with the data from the questions
        with which user has been promped.
        Returns
        -------
        None
        """
        # Base name of the file
        basename = os.path.basename(entrie_full_abs_path)

        # If the file is manifest.json
        if basename == 'manifest.json':
            # Generate new current working directory
            newCWD = os.path.join(self.new_project_dir,
                                  new_entrie_path.split(basename)[0][1:])
            oldCWD = os.getcwd()
            # Get in new current working directory
            os.chdir(newCWD)
            # Populate manifest.json file with the data from users answers
            self.populate_manifest(basename,
                                   os.path.abspath(entrie.absolute()))
            # Reset the current working directory
            os.chdir(oldCWD)
        else:
            # Copy the file from his original directory to his new one
            copyfile(os.path.abspath(entrie.absolute()),
                     os.path.join(self.new_project_dir, new_entrie_path[1:]))

    def copy_files(self, directory=None):
        """Generate vCD UI Plugin from template.
        Paramenters
        -------
        directory | Path

        Returns
        -------
        None
        """

        # Create queue for directories
        q = queue.Queue()
        # Put the start point directory
        q.put(directory)

        # Loop while q is not empty
        while q.empty() is not True:
            # Pop the first element from the queue
            node = q.get()

            # Loop through the node entries
            for entrie in node.iterdir():
                # Split the absolute path
                entrie_full_abs_path = os.path.abspath(entrie.absolute())
                entrie_parts = entrie_full_abs_path.split(self.template_name)
                # Get the relative path to the entrie
                new_entrie_path = entrie_parts[len(entrie_parts) - 1]

                # If entries is file
                if entrie.is_file():
                    self.generate_files(entrie_full_abs_path, new_entrie_path,
                                        entrie)
                # else if it is directory and it isn't node modules
                elif entrie.is_dir() and entrie.name != 'node_modules':
                    # Create the new directory
                    os.mkdir(os.path.join(self.new_project_dir,
                             new_entrie_path[1:]))

                    # Add the entrie to the queue to loop through his
                    # directories if any
                    q.put(entrie)

    def generate(self):
        """Generate vCD UI Plugin from template.
        Returns
        -------
        None
        """

        # Load inital user prompts
        prompts = PromptLauncher([
            Prompt(
                "template_path",
                str,
                message="Please enter a valid absolute template path",
                validator=ValidatorFactory.checkForFolderExistence(),
                err_message="The path has to be valid absolute path"
            ),
            Prompt(
                "projectName",
                str,
                message="Project name",
                default="ui_plugin"
            )
        ])

        # Assign answers
        self.answers = prompts.multi_prompt()
        # Assign template name
        self.template_name = self.answers["template_path"]
        # Construct the path of the new project
        self.new_project_dir = os.path.join(os.getcwd(),
                                            self.answers["projectName"])

        # Indicate that the system search for manifes.json
        spinner = CliSpinner(text="Parse manifest.json", spinner='line')
        spinner.start()

        # Assign manifest.json
        self.manifest = self.parse_manifest()

        # Stop inidaction
        spinner.stop()

        # Load prompts
        prompts.add([
            Prompt(
                "urn",
                str,
                message="Plugin urn",
                default=self.manifest["urn"]
            ),
            Prompt(
                "name",
                str,
                message="Plugin name",
                default=self.manifest["name"]
            ),
            Prompt(
                "containerVersion",
                str,
                message="Plugin containerVersion",
                default=self.manifest["containerVersion"]
            ),
            Prompt(
                "version",
                str,
                message="Plugin version",
                default=self.manifest["version"]
            ),
            Prompt(
                "scope",
                str,
                message="Plugin scope",
                default=self.manifest["scope"]
            ),
            Prompt(
                "permissions",
                str,
                message="Plugin permissions",
                default=self.manifest["permissions"]
            ),
            Prompt(
                "description",
                str,
                message="Plugin description",
                default=self.manifest["description"],
                err_message="""Plugin description has to be greather then 3
                and less then 255 characters""",
                validator=ValidatorFactory.length(0, 255),
            ),
            Prompt(
                "vendor",
                str,
                message="Plugin vendor",
                default=self.manifest["vendor"]
            ),
            Prompt(
                "license",
                str,
                message="Plugin license",
                default=self.manifest["license"]
            ),
            Prompt(
                "link",
                str,
                message="Plugin link",
                default=self.manifest["link"],
                err_message="""The link url is not valid, please enter valid url
                address and with length between 8 - 100 characters.""",
                validator=[
                    ValidatorFactory.length(8, 100),
                    ValidatorFactory.pattern(r'^((http|https)://)')
                ]
            ),
            Prompt("route", str, message="Plugin route",
                   default=self.manifest["route"])
        ])
        # Prompt user
        project_answers = prompts.multi_prompt()

        # Collect answers
        self.answers = {**self.answers, **project_answers}

        # Indicate generating
        spinner = CliSpinner(text="Generate tempalte", spinner='line')
        spinner.start()

        # If this path exists remove it
        if os.path.exists(self.new_project_dir):
            rmtree(self.new_project_dir)

        # Create the directory to given path
        os.mkdir(self.new_project_dir)

        # Start copy files
        self.copy_files(Path(self.answers["template_path"]))

        # Stop inidaction
        spinner.stop("Completed!")
