"""
This module contains utility functions for executing calibration and validation run.

@author: Nels Frazer, Xia Feng
"""

from contextlib import contextmanager
from email.mime.text import MIMEText
from os import getcwd, chdir, PathLike
import smtplib
from typing import Union
from time import sleep
import subprocess
import threading

import logging

from rich.live import Live
from rich.panel import Panel


def _generate_panel(log_file: str, n_lines: int = 10) -> Panel:
    tail_output = subprocess.check_output(f"tail -n {n_lines} {log_file}", shell=True).decode("utf-8")
    panel = Panel(tail_output.strip())
    return panel

class LiveLogPanel:
    def __init__(self, log_file: str, n_lines: int = 10):
        self.log_file = log_file
        self.n_lines = n_lines
        self.stop_threads = False
        self.thread = threading.Thread(target=self.tail_logfile, args=(log_file, n_lines), name="console_log")
        self.thread.start()

    def tail_logfile(self, log_file: str, n_lines: int = 10):
        with Live(_generate_panel(log_file, n_lines), refresh_per_second=4) as live:
            while not self.stop_threads:
                sleep(1)
                live.update(_generate_panel(log_file, n_lines))

    def stop(self):
        self.stop_threads = True
        self.thread.join()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


@contextmanager
def pushd(path: Union[str, PathLike]) -> None:
    """Change current working directory to the given path.

    Parameters
    ----------
    path : New directory path

    Returns
    ----------
    None

    """
    # Save current working directory
    cwd = getcwd()

    # Change the directory
    chdir(path)
    try:
        yield
    finally:
        chdir(cwd)


def complete_msg(basinid: str, run_name: str, path: Union[str, PathLike]=None, user_email: str=None) -> None:
        """Send email notification to user if run is completed.

        Parameters
        ----------
        basinid : Basin ID
        run_name : Calibration or validation run
        path : Work directory
        user_email : User email address

        Returns
        ----------
        None

        """
        if user_email:
            subject = run_name.capitalize()  + ' Run for {}'.format(basinid) + ' Is Completed'
            content = subject + ' at ' + path if path else subject
            msg = MIMEText(content)
            msg['Subject'] = subject
            msg['From'] = 'foo@example.com'
            msg['To'] = user_email
            try:
                server = smtplib.SMTP('foo-server-name')
                server.sendmail(msg['From'], user_email, msg.as_string())
            except Exception as e:
                logging.error(e)
                logging.error('completion email ' + 'for {}'.format(basinid) + "can't be sent")
            finally:
                server.quit()
        else:
            print(content)
