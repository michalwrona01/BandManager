# BandManager

## Description
It is a music band management application.
This is my first application where I used the [Flask](https://flask.palletsprojects.com/en/1.1.x/) framework.

## Technologies
* [Python 3.9.2](https://www.python.org/)
* [Flask 1.1.2](https://flask.palletsprojects.com/en/1.1.x/)
* [SQLAlchemy 1.4.5](https://www.sqlalchemy.org/)
* For stylistic correctness I use [Bootstrap v4.6](https://getbootstrap.com/docs/4.6/getting-started/introduction/)

## Features
- Sing Up
- Login
- Add band
- Delete band
- Add new members to band
- Delete members from band
- Limited features for team members in relation to the team "boss" admin.
- Wallet band
  - Add Donate
  - Add Withdraw
  - Add Expense
  - History transactions
- Orders
  - Add order
  - Display order
- Messeges
  - Send message
  - Receive
  - Sent message
- SongBook
  - Playlist
    - Add playlist
    - Add playlist with add songs
  - Song
    - Add song
    - Add chords to song
      - **Algorithm that changes the musical key half a tone up**
      - **Implement my author's "Attribute Text Editor" convert for example `h1'Hello Wordl'` to `<h1>Hello Wordl</h1>`**
## Presentation
![Alt Text](https://github.com/michalwrona01/BandManager/blob/main/presentation.gif?raw=true)

## My application demo
https://bandmanager-wrona-michal.herokuapp.com/

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install BandManger.

```bash
pip install -r requirements.txt
```
## Start application
```bash
python main.py
```
Enter your browser on this link: http://127.0.0.1:5000/

