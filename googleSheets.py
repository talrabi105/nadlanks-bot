import gspread
import os
import re
import time


class GoogleSheets:
    def __init__(self):
        self.table = []
        self.wa_list = []
        self.m_list = []
        service = gspread.service_account(filename=os.getcwd() + r"\file1.json")
        file = service.open("הלקוחות שלי")
        self.sheet = file.worksheet("sheetForPython")

    def check(self):
        val = None
        while val is None:
            try:
                val = self.sheet.cell(1, 1).value
            except:
                pass

        return int(val)

    def read(self):
        self.update_table()
        for contact in self.table[1:]:
            if re.search("^[0-9+].*", contact[1]):
                self.wa_list.append([contact[0], contact[1]])
            elif contact[1] != ' ':
                self.m_list.append([contact[0], contact[1]])


    def get_msg(self):
        return self.sheet.cell(1, 2).value

    def get_wa_list(self):
        return self.wa_list

    def get_m_list(self):
        return self.m_list

    def get_names_list(self):
        return [self.table[i][0] for i in range(1, len(self.table))]

    def end(self):
        self.sheet.update_cell(1, 1, '0')
        self.wa_list = []
        self.m_list = []

    def update_table(self):
        c = self.sheet.cell(1, 3).value
        table = self.sheet.get("A1:B" + c)
        while len(table) != int(c) or [i for i in table if len(i) != 2]:
            time.sleep(1)
            table = self.sheet.get("A1:B" + c)
        self.table = table
        print(self.table)

    def upload_status(self, contact_details, status):
        for i in range(len(self.table)):
            if self.table[i][1] == contact_details:
                self.sheet.update_cell(i + 1, 3, status)

    def get_first_msg(self):
        fm = self.sheet.get("E1:F1")[0]
        while not (fm[0] and fm[1]):
            fm = self.sheet.get("E1:F1")[0]
        return self.sheet.get("E1:F1")[0]

    def get_current_place(self):
        return self.sheet.cell(1, 4).value