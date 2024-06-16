SELECT name FROM songs where artist_id = (SELECT id FROM artists WHERE name = 'Post Malone');
