CREATE TYPE visibility AS ENUM ('public', 'friends', 'private');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
	visibility visibility NOT NULL
	creation_date DATE NOT NULL,
);

-- This table will be used both to keep track of friend requests and as a friends list
CREATE TABLE friends (
	sender_id INTEGER REFERENCES users NOT NULL,
	recipient_id INTEGER REFERENCES users NOT NULL,
	accepted BOOL NOT NULL,
	UNIQUE (sender_id, recipient_id),
	UNIQUE (recipient_id, sender_id)
);

CREATE TYPE lobby_status AS ENUM ('ingame', 'ready', 'waiting', 'inactive'); 
-- Even inactive lobbies are stored in the database so that chat logs can be checked later
CREATE TABLE lobbies (
	id INTEGER PRIMARY KEY,
	owner_id INTEGER REFERENCES users NOT NULL,
	player2_id INTEGER REFERENCES users,
	status lobby_status NOT NULL,
	visibility visibility NOT NULL,
	spectators_allowed BOOL NOT NULL,
	UNIQUE (owner_id, player2_id),
	UNIQUE (player2_id, owner_id)
	-- Last updated date could be added for automatically removing lobbies that users forgot to close
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
	lobby_id INTEGER REFERENCES lobbies NOT NULL,
    user_id INTEGER REFERENCES users NOT NULL,
    content TEXT NOT NULL,
    sent_at TIMESTAMP NOT NULL
);

CREATE TABLE game_stats (
	winner_id INTEGER REFERENCES users NOT NULL,
	loser_id INTEGER REFERENCES users NOT NULL,
	move_count INTEGER NOT NULL,
	played_on TIMESTAMP NOT NULL
	-- Count of won subboards by each player could be added to this table
);
