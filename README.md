<h3 align="center">Legends Of Runeterra Overseer</h3>

---

<p align="center"> Simple Python data gatherer for the new League of Legends card game legends of runeterra.
    <br> 
</p>


## 📝 Table of Contents
- [Problem Statement](#problem_statement)
- [Idea / Solution](#idea)
- [Dependencies / Limitations](#limitations)
- [Future Scope](#future_scope)
- [Usage](#usage)
- [Authors](#authors)

## 🧐 Problem Statement <a name = "problem_statement"></a>
Riot Games organised a quick hackathon like event to test out their API for their game "Legends of Runeterra". Our task was to create anything we wanted using their API so they could find any flaws and advantages the system had and figure out how to improve it. This competition lasted from November 11th at 10 AM PST until November 22nd at 10 AM PST. The end result will be graded on the following:
- DIFFICULTY: How difficuly was it to create it
- CLARITY/PRESENTATION: How easy is it for someone to pickup and use your product
- POLISH: How close is the project to a finished product
- DOCUMENTATION: How well documented is it (Hense this readme 🧐)

## 💡 Idea / Solution <a name = "idea"></a>
Overseer's purpose will be to satisfy two recurring needs present in competitive card games:
-the lack of a replay feature
-the lack of publicly available statistics.

The app (https://github.com/sjuery/LoRDataGatherer) will run in the background and access the Legends of Runeterra API, sending valuable information such as the deck code, rectangle positions, and game states to an online database where the data will be processed, organized and made accessible to players through a website. Once logged in, players will be able to review their match history and a detailed replay of any selected event with a wealth of valuable data. The site will provide access to a large variety of statistics such as - among others - the average winrate of a region, deck, or card. This will allow players with an account to compare themselves to the average player (and in the future the average player of a specific rank) and to analyze their strengths and weaknesses in order to most efficiently use the replay feature and improve their skills.

The pitch for the app can be found here (https://gist.github.com/sjuery/b8cca22c480d1b3a76cfc90a77cb0e0b)

The website (https://loroverseer.herokuapp.com/), was create with python and django and stores its statistics using Postgres and AWS S3.

The main information the website stores are stored under using django models on Postgres:

* Game:
    * User (Primary Key, User Model of the Host Found using the secretKey)
    * Player (string containing the host players username)
    * Opponent (string containing the current games opponent)
    * DeckCode (string containing the deck of the host during this game)
    * GameMode (string with either "Normal", "Ranked", or "Expedition")
    * Regions (string with the region mixes found in the players deck 2 regions if normal or ranked, 3 if expedition)
    * ExpeditionWins (int with the amount of wins in the current expedition)
    * ExpeditionLosses (int with the amount of losses in the current expedition)
    * Win (boolean that returns true if the host won the match)
    * DatePlayed (Date and time the game was played at)

* Region:
    * Name (Primary Key, Name of each region combinations found seperated by a +)
    * NormalWins (integer with the amount of wins said region has had in normal mode)
    * NormalTotal (integer with the amount of total games said region has had in normal mode)
    * ExpeditionWins (integer with the amount of wins said region has had in expedition mode)
    * ExpeditionTotal (integer with the amount of total games said region has had in expedition mode)

* Deck:
    * Code (Primary Key, string with the deckCode)
    * Regions (string with the region combinations of said deck. seperated by a +)
    * Wins (integer with the total wins with this deck No need to track what mode this deck comes from 40 cards means normal mode, less then that means expeditions)
    * TotalGames (integer with the total games played with this deck)

* Card:
    * ID (Primary Key, string with the ID the card)
    * NormalWins (integer with the amount of wins said card has had in normal mode)
    * NormalTotal (integer with the amount of total games said card has had in normal mode)
    * ExpeditionWins (integer with the amount of wins said card has had in expedition mode)
    * ExpeditionTotal (integer with the amount of total games said card has had in expedition mode)
    
The rectangle position for each games are stored in JSON files on Amazon Web Services. Their structure is somewhere along those lines:
```
    {
        frame0:
        {
            [
                "CardID": 0,
                "CardCode": "01DE001",
                "TopLeftX": 800,
                "TopLeftY": 900,
                "Width": 252,
                "Height": 373,
                "LocalPlayer": true
            ],
            ...
        },
        frame1:
        {
            ...
        }
    }
```

## ⛓️ Dependencies / Limitations <a name = "limitations"></a>
The python version of the project has the following dependencies:

All of these can be found in the requirments.txt file

## 🚀 Future Scope <a name = "future_scope"></a>
Gonna fill this in after the project is over because the deadline is almost up

## 🎈 Usage <a name="usage"></a>
Simply go to the following link:
https://loroverseer.herokuapp.com/

Creating an account will allow you to track your Legends of Runeterra games using this app (https://github.com/sjuery/LoRDataGatherer)

Accessing the website without an account will still allow you to see general statistics on all games played with the app running.

## ⛏️ Built With <a name = "tech_stack"></a>
- [Python](https://www.python.org/) - Python
- [Django](https://www.djangoproject.com/) - DJango
- [AWS](https://aws.amazon.com/) - AWS

## ✍️ Authors <a name = "authors"></a>
- [@sjuery](https://github.com/sjuery)
