Discord Bot running on Heroku.

accessing the database:
psql --host=ec2-52-44-13-158.compute-1.amazonaws.com --port=5432 --username=aarrjkfacqwgqc --password --dbname=d3oe0vsvoenbff


create table:
CREATE TABLE tezos_wallets (
id serial PRIMARY KEY,
user_id VARCHAR (50) NOT NULL,
tezos_wallet VARCHAR (50) NOT NULL,
);


launch dyno from terminal
heroku ps:scale worker=1 -a discord-wallet-bot
