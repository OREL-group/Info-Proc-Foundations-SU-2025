# # Imports the requests dictionary to pull words from the Google Books API, and
# the random dictionary to pick a random word for each round of the game.
import requests
import random

# # This section of the code pulls titles from the Google Books API based on a
# given search term, input by the user.

api_key = "AIzaSyCZNWM276KQiNOq1Z30t57qApvnX1pKqTc"
query = "intitle:", input("To begin the game, enter a search term to send to Google Books: ")
url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"

response = requests.get(url)
data = response.json()

###############################################################################

# # This section of the code implements the "Hangman" game. The player guesses a
# random word pulled from the list of Google Books titles pulled in the previous
# section.


# # This section sets up the elements that will be used in the game. It creates
# an array and populates it with strings of titles pulled from the above input
# Google Books search. Then randomly picks one title from that list to be put
# into play, and creates the empty spaces to be displayed to the player.
# Finally, it creates the guesses_left countdown, which is tested to see if the
# player has reached the fail state and the game ends.

wordBank = []
for item in data.get('items', []):
  stepThroughTitles = item['volumeInfo'].get('title')
  wordBank.append(stepThroughTitles)
wordInPlay = random.choice(wordBank)
displayed_word = ["_" for _ in wordInPlay]
guesses_left = 5 ## sets the max number of incorrect guesses before the game ends to 5


# # This segment preemptively catches non-alphabetical characters and fills them
# in before the game starts.

specialCharacters = [" ", "!", "?", ",", "-", ":", ";", "—", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
for i in range(len(wordInPlay)): 
  if wordInPlay[i] in specialCharacters:
    displayed_word[i] = wordInPlay[i]

# # This segment asks the player for an input of a letter, and then steps
# through the wordInPlay to check if that letter exists within it. The loop
# replaces "_" underscores with the guessed letter. It also catches upper and
# lower cases, so the guessing game is not case-sensitive. If the player guesses
# incorrectly, the guesses_left counter is lowered by 1. The game ends when
# guesses_left reaches 0 (fail state), or the word is filled in (win state).
# Finally, the code prints a winning or losing message.

while guesses_left > 0 and "_" in displayed_word:
  print("\n Title: ", " ".join(displayed_word))
  guess = input("\n Guess a letter: ")
  guessLower = guess.lower() 
  guessUpper = guess.upper() ## splits input into lower and upper case variants to avoid case sensitivity in the letter matching
  if guessLower in wordInPlay or guessUpper in wordInPlay: ## runs through the word once to check for lower case, then again for upper case. I suspect there's a more efficient way to do this.
    for i in range(len(wordInPlay)):
      if wordInPlay[i] == guessLower:
        displayed_word[i] = guessLower
      if wordInPlay[i] == guessUpper:
        displayed_word[i] = guessUpper
  else:
    guesses_left -= 1
    print("\n Nope.", guesses_left, "guess(es) left. \n")

if "_" not in displayed_word:
  print("\n Congratulations! \n The title was:", wordInPlay)
else:
  print("\n You're out of guesses! Game over. \n The title was:", wordInPlay)

###############################################################################
