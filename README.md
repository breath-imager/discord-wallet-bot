Discord Bot 🤖 running in background on Heroku. Uses PostgreSQL running on heroku to store and update tezos wallets of Season pass holders role.



Features:
help - explains how to add a wallet
add <tezos wallet address> - adds user's tezos wallet to the database
update <tezos wallet address> - updates user's tezos wallet address on the database
  
Other features:
- Oblique Strategies card-model can be activated using keywords !eno, !os, !oblique !strategies
- Hello, gm are pre-programmed to reply. gm only 20% of the time.

  
  

Accessing the postgres database:
-------------------------------  
psql --host=ec2-52-44-13-158.compute-1.amazonaws.com --port=5432 --username=aarrjkfacqwgqc --password --dbname=d3oe0vsvoenbff

SQL commands
  
create table:
CREATE TABLE tezos_wallets (
id serial PRIMARY KEY,
user_id VARCHAR (50) NOT NULL,
tezos_wallet VARCHAR (50) NOT NULL,
);


Launching Dyno from terminal
-------------------------------  
heroku ps:scale worker=1 -a discord-wallet-bot
