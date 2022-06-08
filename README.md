# Rasa based chatbot in Python
Third assignment for Scripting languages classes.

Prerequisites:
 Discord bot -> create .env file in the discordAPI directory and set DISCORD_TOKEN
 Discord library -> __pip install discord.py__
 Rasa library -> __pip install rasa__
 
 How to run:
  Three command line windows with the following commands sequentially in them:
  - rasa run actions
  - rasa shell
  - python3 discordAPI/chatbot.py
 
Chatbot allows you to check schedule for invented tournaments, see what games will be played, and add player to a tournament for a specific game. 
When a player is added to a tournament, they are given a number and start time information.
