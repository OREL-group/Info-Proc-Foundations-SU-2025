#actions main menu
def start_menu():
   print('''
Spencer Mansion Text Adventure
++++======================++++

Within a forest outside the city limits, you were being chased by Zombie dogs and
have taken shelter in a mansion. Grab as many items as you can but beware the Tyrant!

How to move:
Type 'go' & then [cardinal direction]
How to grab items:
Type 'get' & then [named item]

To Exit:
Type 'quit'
''')


#staus of locations and inventory
def status_screen():
   print('++++======================++++')

   #room status
   print('You are in the ' + current_room)
   #inventory status
   print('Inventory : ' + str(inventory))
   #message for item
   if "item" in rooms[current_room]:
       print('You see a ' + rooms[current_room]['item'])
   #message for note
   elif "note" in rooms[current_room]:
       print('You see a note! It says, ' + rooms[current_room]['note'])

   print("++++======================++++")

#creating an empty inventory with a list
inventory = []

#dictionary for rooms, adjacent rooms, and notes & items
#rooms must be uppercase, and items must be lowercase
rooms = {
   'Front Lawn': {
       'north': 'Main Hall',
       'item': 'zombie dogs'
   },
   'Main Hall': {
       'north': 'Rear Gated Garden',
       'south': 'Front Lawn',
       'east': 'East Hallway',
       'west': 'Dining Room'
   },
   'Dining Room': {
       'north': 'Kitchen',
       'east': 'Main Hall',
       'west': 'Den',
       'item': 'salt'
   },
   'Den': {
       'east': 'Dining Room',
       'note': '"Find the polished key and go to Rear Gated Garden."'
   },
   'Kitchen': {
       'south': 'Dining Room',
       'west': 'Pantry',
       'note': '"To polish any surface all you need is vinegar, salt, and water!"'
   },
   'Pantry': {
       'east': 'Kitchen',
       'item': 'vinegar'
   },
   'East Hallway': {
       'north': 'Master Bedroom',
       'south': 'Study',
       'east': 'Bathroom',
       'west': 'Main Hall'
   },
   'Master Bedroom': {
       'south': 'East Hallway',
       'item': 'rusty key'
   },
   'Bathroom': {
       'west': 'East Hallway',
       'item': 'water jug'
   },
   'Rear Gated Garden': {
       'south': 'Main Hall'
   },
   'Study': {
       'north': 'East Hallway',
       'item': 'tyrant'
   }
}

#start room location
current_room = 'Main Hall'
#keep instructions outside loop so it only displays once
start_menu()


#loops until condition is false (win/lose conditions or exit)
while True:
   #keep within loop so it displays indefinitely
   status_screen()

   #splitting a string to index it for movement & item management
   move = ''
   while move == '':
       #'>' added to see where to type input
       move = input('>')
       #lower() is used to covert uppercase to lowercase
   move = move.lower().split(" ", 1)

   #inputs that determine how you navigate the mansion
   #checks if 'go' is first input (lists begin at 0)
   if move[0] == 'go':
       #checks to see if there is a 'room' in the chosen direction
       if move[1] in rooms[current_room]:
           #rooms are mutable, swaps current room to the new one
           current_room = rooms[current_room][move[1]]
       #if there is no 'room' in the chosen direction then print message
       else:
           print('You can\'t go that way!')

   #again, checks to see if 'get' was input first
   if move[0] == 'get':
       #checks if current room contains an item and if the item is the written
       #'and', boolean operator that can only comeback true if both values are true
       if "item" in rooms[current_room] and move[1] in rooms[current_room]['item']:
           #inventory is mutable, adds second index('item') to inventory
           inventory.append(move[1])
           print(move[1] + ' placed in inventory!')
           #removes the item from current room to avoid confusion
           del rooms[current_room]['item']
       #if the item isn't in room, print message
       else:
           print("Can't get " + move[1] + '!')


   #conditions to win:
   #all item combo & rear garden path
   if (current_room == 'Rear Gated Garden' and
           'rusty key' in inventory and 'salt' in inventory and 'vinegar' in inventory and 'water jug' in inventory):
       print('You combined the Vinegar, Salt, and Water Jug into a Anti-Rust remover!\n'
             'This with the Rusty Key now becomes a Polished Key! You use this to escape!...YOU WIN!')
       break

   #conditions to lose:
   #front lawn: zombie dogs
   elif 'item' in rooms[current_room] and 'zombie dogs' in rooms[current_room]['item']:
       print('The Zombie Dogs surround you!...GAME OVER!')
       break
   #study: tyrant
   elif 'item' in rooms[current_room] and 'tyrant' in rooms[current_room]['item']:
       print('You have fallen to the Tyrant...GAME OVER!')
       break


   #exiting game early
   if move[0] == 'quit':
       print()
       print("Thank you so much a-for-to playing my game!")
       break
