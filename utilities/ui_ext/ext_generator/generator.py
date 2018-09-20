import os, queue

from abc import ABC, abstractmethod, abstractstaticmethod
from pathlib import Path

class Generator(ABC):
    @property
    def answers(self):
        """Getter for answers property.
        Returns
        -------
        answers : dict
        """

        return self._answers
    
    @answers.setter
    def answers(self, answers):
        """Setter for answers property.
        Returns
        -------
        answers : dict
        """

        self._answers = answers

    @property
    def template_name(self):
        """Getter for template_name property.
        Returns
        -------
        template_name : str
        """

        return self._template_name
    
    @template_name.setter
    def template_name(self, template_path):
        """Setter for template_name property.
        Returns
        -------
        template_name : str
        """

        # Split the absolute template path
        templates_path_parts = template_path.split("/ui/")
        # Assign template name
        self._template_name = templates_path_parts[len(templates_path_parts) - 1]

    @property
    def new_project_dir(self):
        """Getter for new_project_dir property.
        Returns
        -------
        new_project_dir : str
        """

        return self._new_project_dir
    
    @new_project_dir.setter
    def new_project_dir(self, new_project_dir):
        """Setter for new_project_dir property.
        Returns
        -------
        new_project_dir : str
        """

        self._new_project_dir = new_project_dir

    @abstractmethod
    def generate(self):
        """Generate vCD UI Plugin from template.
        Returns
        -------
        None
        """   
        pass

    def binary_search_file_by_name(self, alist, item):
        """Find file with given name in list of files.
        Returns
        -------
        file : Path
        """
        first = 0
        last = len(alist) - 1
        found = False
        
        while first <= last and not found:
            midpoint = int((first + last) / 2)

            if os.path.basename(os.path.abspath(alist[midpoint].absolute())) == item:
                found = alist[midpoint]
            else:
                if item < alist[midpoint].name:
                    last = midpoint - 1
                else: first = midpoint + 1
        
        return found

    def find_file(self, rootPath, fileName):
        """Find file with given name in given root directory.
        Returns
        -------
        file : Path
        """
        q = queue.Queue()
        q.put(Path(rootPath))

        while q.empty() is False:
            node = q.get()

            found = self.binary_search_file_by_name(list(node.iterdir()), "manifest.json")

            if found is False:
                for entrie in node.iterdir():
                    if entrie.is_dir():
                        q.put(entrie)
            else:
                return found