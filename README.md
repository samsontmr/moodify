# moodify

## Inspiration
We often find it difficult to express our feelings in words. However, the human face does this effortlessly. We want to use the power of deep learning to read these emotions and recommend the perfect playlist for your mood.

moodify, powered by emotion. 

## What it does
Send our Telegram bot [@moodifybot](telegram.me/moodifybot) a selfie and it will recommend a playlist to suit your mood!

## How we built it
moodify was built during a HacknRoll 2017. We leveraged the power of Microsoft Cognitive Services to detect a person's mood from their facial expression, used that information to choose a Spotify playlist, and packaged it up into an easy-to-use Telegram bot.

* APIs, Services
  * Microsoft Emotion API
  * Telegram Bot API with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
  * Spotify WebAPI
  * Heroku

## What's next for moodify
Generating custom playlists using machine learning

## We Welcome Pull Requests
* moodify uses API tokens to communicate with the different servers, and I unfortunately am unable to share them here. However, these services are free for limited use.
