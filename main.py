from classes import Estate

estate = Estate.load_estate('Dantill')

character_titles = [char.title for char in estate.characters.values()]

# estate.start_event('story', 'The Old Road')
# estate.start_event('story', 'Crash')



# estate.encounter(event_type = 'story', event_title='Vermin', enemies=['Brigand Cutthroat'])
estate.characters['Highwayman'].fast_status_description(3, 8, 'Irrational')
estate.characters['Heir'].fast_status_description(2, 10, 'Selfish')
estate.characters['Heiress'].fast_status_description(4, 10, 'Paranoid')
estate.characters['Crusader'].fast_status_description(5, 5, 'Hopeless')
estate.encounter(event_type = 'story', event_title='Vanquished', enemies=['Brigand Cutthroat', 'Brigand Bloodletter', 'Brigand Fusilier', 'Brigand Fusilier'])