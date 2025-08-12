=====GUESS THE GOOGLE BOOK=====
Brock McCord
IS 430

---I. OVERVIEW---

This program runs a simple "guess the letters," or "Hangman" game. The player will be prompted to enter a search term. This term is sent to the Google Books API. 
An array of titles are returned, and one of these titles is chosen at random to be the word in play.

---II. INSTRUCTIONS---

When the program begins, the user will be prompted to enter a search term into Google Books.

Afterwards, the Hangman game will begin. Empty spaces will be displayed, representing the spaces of letters in the title.

Enter one letter at a time. Your input does not need to be case-sensitive.

The player should only enter letters in the alphabet. Special characters such as punctuation, numbers, and spaces will be filled in automatically.

---III. PROGRAM LIMITATIONS---

There are some technical limitations to the project: it does not have any "navigation" commands, such as exiting or repeating the game. 
The program must be terminated manually to stop it mid-game. Likewise, the program will terminate once the game is over, and must be relaunched to play again.
These features could be added to the program with minimal difficulty, if the project were to go further.

As noted during the project presentation, although the code functions as intended, the quality of the game itself is quite limited. 
In particular, the player entering their own search term gives them a hint for at least one of the words in the title. 
This could be rectified by providing the player with a list of "categories," compiled from the Google Books metadata, and sorting by that instead. 
As someone noted during the presentation, you might play this with two people, and have one enter the search phrase, while the other guesses. 

---IV. PROJECT REFLECTION---

This project began primarily in search of a beginner coding project that I felt capable of working through. Although I work in library technical services, my role requires no coding, and I have next to no experience with it.
Although not particularly relevant to information sciences or library work, I felt that a simple command prompt game would be suitably simple project, while also having the satisfaction of creating a "fun" end product.
The game structure also allowed for easy testing, with satisfying results, as it inherently involves inputs, processes, and outputs which can be observed as working properly or not.

I began by making a natural language framework for what I'd expect to need to make a Hangman game, and then added coding elements. 
For example, a list of strings for a word bank, a randomization dictionary, a loop which would call for inputs and check against the chosen word, etc.
As I wasn't familiar with Python syntax, I would search for coding examples of these concepts, and then adapt what I found to my needs. 
The end result was a very simple, and not particularly long, block of code.

As the game felt very simple, I felt I should go one step further and add an extra element. 
For the nominal sake of relevance to information sciences, I decided to integrate the Google Books API to populate the word bank of potential words to guess.
This required creating a Google Books account, generating an API key, importing the requests dictionary in Python, and determining how to send the query and store the results I wanted.
Somewhat ironically, although this block of code is even smaller than the body of the game loop, it took significantly longer to create and troubleshoot.
Information on Google Books API integration felt more "advanced," for lack of a better word, and more difficult to find and implement, than the simple Python functions in the game.

Of course, the finished product is hardly viable as any sort of product or tool to bring to library sciences.  
For the sake of imagination, I could see a more advanced version of a game like this integrated into something like a library's website as a way to engage a user. 
A game which pulls a random selection from something like a special collection's catalog and has the player uncover it could be utilized to show patrons the variety of interesting titles.
This function is not dissimilar to something like Google's "I'm feeling lucky" button, or tools which take the user to a random Wikipedia page. 

While the product itself might not have much relevance to my future work in library sciences, I'm pleased with the process and final product. 
The choice of a game kept the process entertaining and light hearted, and gave what otherwise might have been a daunting project an air of playfulness.
I do believe that this was a good learning experience, both in providing a simple problem to work through, and reinforcing basic coding practices. 
