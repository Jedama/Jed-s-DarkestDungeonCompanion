from classes import Estate
from storage import SaveEditor

def wsl_path(windows_path):
    """Convert a Windows path to a WSL-accessible path."""
    return '/mnt/c' + windows_path[2:].replace('\\', '/')

editor = SaveEditor(wsl_path(r"C:\repos\DarkestDungeon\JedsDDCompanion\include\DarkestDungeonSaveEditor-master\build\libs\DDSaveEditor.jar"))

save_data = editor.decode_save(wsl_path(r"C:\Program Files (x86)\Steam\userdata\86795628\262060\remote\profile_3\persist.roster.json"), output_file=wsl_path(r"C:\repos\DarkestDungeon\JedsDDCompanion\savereader\town.json"))
print(save_data)


estate = Estate.load_estate('Dantill')

title, story, consequences = estate.start_event(event_title='Argument4')

estate.recruit('Offering', ['Slow', 'Pallid'])

estate.save_estate()

character_titles = [char.title for char in estate.characters.values()]

# estate.start_event('story', 'The Old Road')
# estate.start_event('story', 'Crash')



# estate.encounter(event_category = 'story', event_title='Vermin', enemies=['Brigand Cutthroat'])
estate.characters['Highwayman'].fast_status_description(3, 8, 'Irrational')
estate.characters['Heir'].fast_status_description(2, 10, 'Selfish')
estate.characters['Heiress'].fast_status_description(4, 10, 'Paranoid')
estate.characters['Crusader'].fast_status_description(5, 5, 'Hopeless')
estate.encounter(event_category = 'story', event_title='Vanquished', enemies=['Brigand Cutthroat', 'Brigand Bloodletter', 'Brigand Fusilier', 'Brigand Fusilier'])