CREATE TYPE stats_visibility AS ENUM ('public', 'friends', 'private');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
	stats_visibility stats_visibility NOT NULL
);

-- This table will be used both to keep track of friend requests and as a friends list
CREATE TABLE friends (
	sender_id INTEGER REFERENCES users NOT NULL,
	recipient_id INTEGER REFERENCES users NOT NULL,
	accepted BOOL NOT NULL,
	UNIQUE (sender_id, recipient_id),
	UNIQUE (recipient_id, sender_id)
);

-- Even inactive lobbies are stored in the database so that chat logs can be checked later
CREATE TABLE lobbies (
	id SERIAL PRIMARY KEY,
	owner_id INTEGER REFERENCES users NOT NULL,
	player2_id INTEGER REFERENCES users NOT NULL,
	spectator_count INTEGER NOT NULL,
	active BOOL NOT NULL,
	UNIQUE (owner_id, player2_id),
	UNIQUE (player2_id, owner_id)
	-- Last updated date could be added to make automatically removing lobbies that users forgot to close
);

-- I will probably not store the game state in the database
-- I think that would be just bad design, because I will need 3 different representations for the game state already:
	-- a server-side in memory representation using Python (for checking the game logic) 
	-- an in memory representation on the client (for rendering the board)
	-- a representation that can be sent from the client to the server (for updating the client with the other players moves)

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
	lobby_id INTEGER REFERENCES lobbies NOT NULL,
    user_id INTEGER REFERENCES users NOT NULL,
    content TEXT NOT NULL,
    sent_at TIMESTAMP NOT NULL
);

CREATE TYPE player_number AS ENUM ('1', '2');

CREATE TABLE game_stats (
	winner_id INTEGER REFERENCES users NOT NULL,
	loser_id INTEGER REFERENCES users NOT NULL,
	move_count INTEGER NOT NULL,
	played_on TIMESTAMP NOT NULL
	-- Count of won subboards by each player could be added to this table
);
