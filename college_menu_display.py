import re
import pandas as pd

from datetime import datetime as dt, date

menu_excel_sheet_path = r"NEW MENU 2022.xlsx"
menu_book = pd.ExcelFile(menu_excel_sheet_path)

months = {
  "0": [
    "jan",
    "january"
  ],
  "1": [
    "feb",
    "february"
  ],
  "2": [
    "mar",
    "march"
  ],
  "3": [
    "apr",
    "april"
  ],
  "4": [
    "may"
  ],
  "5": [
    "jun",
    "june"
  ],
  "6": [
    "jul",
    "july"
  ],
  "7": [
    "aug",
    "august"
  ],
  "8": [
    "sep",
    "sept",
    "september"
  ],
  "9": [
    "oct",
    "october"
  ],
  "10": [
    "nov",
    "november"
  ],
  "11": [
    "dec",
    "december"
  ]
}

month_names = []
[month_names.extend(i) for i in months.values()]

def timediff(datetime_time_1, datetime_time_2):
    common_date = date(1, 1, 1)
    return abs(dt.combine(common_date, datetime_time_2) - dt.combine(common_date, datetime_time_1)).total_seconds()

def remove_ordinality(number_name):
    # Source: https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string
    rep = {"st": "",
           "nd": "",
           "rd": "",
           "th": ""} # defined replacements here
    # use these three lines to do the replacement
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    #Python 3 renamed dict.iteritems to dict.items so use rep.items() for latest versions
    pattern = re.compile("|".join(rep.keys()))
    number_name = pattern.sub(lambda m: rep[re.escape(m.group(0))], number_name)
    return number_name

# for sheet in menu_book.sheet_names:
#     sheet = sheet.strip().lower().replace('to', '').split()
#     sheet_joined = ''.join(sheet)

#     match = re.match(r"([0-9]*)([a-z]*)([0-9]*)([a-z]*)", sheet_joined, re.I)
#     if match:
#         _ = match.groups()
#         # remove_ordinality(match)
#     # for i in months:
#     #     if . in month_names:
#     #         print(month_names)

# To be changed

mess_active = True
menu_sheet = menu_book.sheet_names[-1]

mess_menu = menu_book.parse(menu_sheet)
mess_menu = mess_menu.drop(mess_menu.columns[[0]], axis=1)
mess_menu = mess_menu.values.tolist()
mess_menu = {
    "breakfast": [i[dt.now().weekday()] for i in mess_menu[3:15]],
    "lunch": [i[dt.now().weekday()] for i in mess_menu[17:26]],
    "hitea": [i[dt.now().weekday()] for i in mess_menu[29:31]],
    "dinner": [i[dt.now().weekday()] for i in mess_menu[33:41]]
}

menu_timings_by_type = {
  'breakfast': (dt.strptime('07:30', '%H:%M').time(), dt.strptime('09:30', '%H:%M').time()),
  'lunch': (dt.strptime('12:00', '%H:%M').time(), dt.strptime('14:30', '%H:%M').time()),
  'hitea': (dt.strptime('17:00', '%H:%M').time(), dt.strptime('18:00', '%H:%M').time()),
  'dinner': (dt.strptime('19:30', '%H:%M').time(), dt.strptime('21:30', '%H:%M').time()),
}

def show_menu():
  # current_time = dt.strptime('9:31', '%H:%M').time() # TODO: Test check, remove later
  current_time = dt.now().time()

  if current_time < menu_timings_by_type["breakfast"][0] and timediff(menu_timings_by_type["breakfast"][0], current_time) > 3600:
    mess_active = False

  elif current_time <= menu_timings_by_type["breakfast"][1]:
    current_menu_type = "breakfast"

  elif current_time <= menu_timings_by_type["lunch"][1]:
    current_menu_type = "lunch"

  elif current_time <= menu_timings_by_type["hitea"][1]:
      current_menu_type = "hitea"

  elif current_time <= menu_timings_by_type["dinner"][1]:
      current_menu_type = "dinner"

  else:
      mess_active = False

  if mess_active:
      current_mess_menu = mess_menu[current_menu_type]
      print(f"Menu for {current_menu_type} -- {dt.now().strftime('%d/%m/%y - %A - %I:%M %p')}")
      print('='*56)
      for i in current_mess_menu:
          if not isinstance(i, float):
              print(i.strip().upper())

  else:
    print("Mess has closed boii, go home :)")

if __name__ == "__main__":
  show_menu()
