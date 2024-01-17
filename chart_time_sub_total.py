from email_reader import emails_from_sender
import pandas as pd
from matplotlib import pyplot as plt
from upgrade_transfer_data_timers import get_credentials, get_sheets


class TimerAnalizer:
    def __init__(self):
        self.credentials = get_credentials()
        self.sheets = get_sheets(self.credentials)

    def show_sheets(self):
        print(sheets)
