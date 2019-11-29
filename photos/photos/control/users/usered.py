import sql
import os

g_cur_path = os.path.abspath(os.path.split(__file__)[0])

def HasAdmin():
  if os.path.isfile(g_cur_path + '../../../db.sqlite3') == False:
    return False
  return True
