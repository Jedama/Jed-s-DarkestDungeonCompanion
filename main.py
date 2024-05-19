from classes import Estate, Event

estate = Estate('Dantill')
estate.start_campaign()

event_story, event_consequences = estate.recruit('Vestal', ['Irrepressible', 'Musical', 'Anemic', 'Fear of Beasts'])

# event_story, event_consequences = estate.start_event('story', 'The Old Road')

# print(event_story)
# print(event_consequences)

# event_story, event_consequences = estate.start_event('story', 'Crash')

# print(event_story)
# print(event_consequences)