import os
os.chdir('../src/')
from managers import data_manager

data_manager.start()
print(data_manager.is_council("257165020"))
print(data_manager.council_ids())
print(data_manager.id_to_names("257165020"))
print(data_manager.names_to_id("диме"))
print(data_manager.names_to_id("мезенцеву"))
