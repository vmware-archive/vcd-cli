import threading
import time
import sys
from enum import Enum

Spinners = Enum('Spinners', {
    "line": {
        "interval": 130,
        "frames": [
            "-",
            "\\",
            "|",
            "/"
        ]
    },
    "dots": {
        "interval": 500,
        "frames": [
            ".",
            "..",
            "..."
        ]
    }
})


def backspace(n):
    # print((b'\x08').decode(), end='')     # use \x08 char to go back
    print('\r', end='')


class CliSpinner:
    """CliSpinner library.
    Attributes
    ----------
    CLEAR_LINE : str
        Code to clear the line
    """
    CLEAR_LINE = '\033[K'

    def __init__(self, text=None, spinner='dots', placement='left',
                 stream=sys.stdout):
        """Constructs the CliSpinner object.
        Parameters
        ----------
        text : str, optional
            Text to display while spinning.
        spinner : str|dict, optional
            String or dictionary representing spinner. String can be one
            of 2 spinners supported.
        placement: str, optional
            Side of the text to place the spinner on. Can be `left` or `right`.
            Defaults to `left`.
        stream : io, optional
            Output.
        """
        self._spinner = Spinners[spinner].value
        self.text = text
        self._stop_spinner = None
        self._interval = self._spinner['interval']
        self._stream = stream
        self._frame_index = 0
        self._placement = placement

    def clear(self):
        """Clears the line and returns cursor to the start.
        of line
        Returns
        -------
        self
        """
        self._stream.write('\r')
        self._stream.write(self.CLEAR_LINE)

        return self

    def _frame(self):
        """Builds and returns the frame to be rendered
        Returns
        -------
        frame
        """
        frame = self._spinner['frames'][self._frame_index]
        self._frame_index += 1

        if self._frame_index == len(self._spinner['frames']):
            self._frame_index = 0

        return frame

    def _render_frame(self):
        """Renders the frame on the line after clearing it.
        """
        frame = self._frame()

        if self.text is not None:
            output = u'{0} {1}'.format(*[
                (self.text, frame)
                if self._placement == 'right' else
                (frame, self.text)
            ][0])
        else:
            output = '{0}'.format(frame)
        self._stream.write(output)
        backspace(len(output))

    def _render(self):
        """Runs the render until thread flag is set.
        Returns
        -------
        self
        """
        while not self._stop_spinner.is_set():
            self._render_frame()
            time.sleep(0.001 * self._interval)

        return self

    def start(self, text=None):
        """Starts the spinner on a separate thread.
        Parameters
        ----------
        text : None, optional
            Text to be used alongside spinner
        Returns
        -------
        self
        """
        if text is not None:
            self.text = text

        self._stop_spinner = threading.Event()
        self._spinner_thread = threading.Thread(target=self._render)
        self._spinner_thread.setDaemon(True)
        self._render_frame()
        self._spinner_id = self._spinner_thread.name
        self._spinner_thread.start()
        
        return self

    def stop(self, message=None):
        """Stops the spinner and clears the line.
        Returns
        -------
        self
        """
        if self._spinner_thread:
            self._stop_spinner.set()
            self._spinner_thread.join()

        self._frame_index = 0
        self._spinner_id = None
        self.clear()

        if message is not None:
            print(message)

        return self
