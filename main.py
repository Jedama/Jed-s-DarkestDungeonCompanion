from classes import Estate
from storage import SaveEditor, ConfigManager

config_manager = ConfigManager("config.json")
editor = SaveEditor(config_manager)

estate = Estate('Debug')
estate.start_campaign()


# estate.start_event('story', 'The Old Road')
# estate.start_event('story', 'Crash')

# estate.encounter(event_category = 'story', event_title='Vermin', enemies=['Brigand Cutthroat'])
estate.characters['Highwayman'].fast_status_description(3, 8, 'Irrational')
estate.characters['Heir'].fast_status_description(2, 10, 'Stalwart')
estate.characters['Heiress'].fast_status_description(4, 10, 'Paranoid')
estate.characters['Crusader'].fast_status_description(5, 5, 'Hopeless')
#title, story, consequences, log = estate.encounter(event_category = 'story', event_title='Vanquished', enemies=['Brigand Cutthroat', 'Brigand Bloodletter', 'Brigand Fusilier', 'Brigand Fusilier'], modifiers=['Dismas took a fierce dagger hit protecting Percival, shooting his attacker with his flintlock point blank.'])

estate.log_dungeon.append('The party survived a vicious ambush on the Old Road, narrowly defeating a group of brigands')
estate.log_dungeon.append('Dismas sustained a serious injury while protecting Percival during the fight')

title, story, consequences, log = estate.divide_loot(8000, ["Hunter's mask", "Severed finger", "Blinding powder", "Stunning stone"])

print(title)
print(story)
