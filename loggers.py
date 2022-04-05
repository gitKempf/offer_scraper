import time
import shutil

terminal_x, _ = shutil.get_terminal_size((80, 20))


def rprint(line):
    print('\r{:{width}}'.format(line, width=terminal_x), end='')


LOGING_STATUS = {
    'log_warnings': False,
    'log_events': True,
    'log_extended_info': False
}


def log_warnings(warning_text):
    if LOGING_STATUS['log_warnings']:
        print(warning_text)


def log_events(event_text):
    if LOGING_STATUS['log_events']:
        rprint(event_text)


def log_extended_info(extended_info_text):
    if LOGING_STATUS['log_extended_info']:
        print(extended_info_text)

