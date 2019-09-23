import sqlite3
import xml.etree.ElementTree as ET

def find_field(traki, wanted_field):
    found = False
    for tag in traki:
        if not found:
            if(tag.tag == "key" and tag.text == wanted_field):
                found = True
        else:
            return tag.text
    return False

conn = sqlite3.connect('Database.db')
cursor = conn.cursor()


create_artist = """CREATE TABLE Artist (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);
"""
create_genre = """CREATE TABLE Genre (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);
"""

create_album= """CREATE TABLE Album (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    title TEXT UNIQUE,
    FOREIGN KEY (artist_id)
    REFERENCES Artist(id)  
);
"""

create_track = """CREATE TABLE Track (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id INTEGER,
    genre_id INTEGER,
    len INTEGER, 
    rating INTEGER, 
    count INTEGER
);
"""

del_artist="""DROP TABLE IF EXISTS Artist;"""
del_album = """DROP TABLE IF EXISTS Album;""" 
del_genre = """DROP TABLE IF EXISTS Genre;"""
del_track = """DROP TABLE IF EXISTS Track;"""

cursor.execute(del_artist)
cursor.execute(del_album)
cursor.execute(del_genre)
cursor.execute(del_track)

cursor.execute(create_artist)
cursor.execute(create_album)
cursor.execute(create_genre)
cursor.execute(create_track)


root = ET.parse('Library.xml').getroot()

tracks_data = root.findall("dict/dict/dict")
for track in tracks_data:
    title = find_field(track, "Name")
    artist = find_field(track, "Artist")
    genre = find_field(track, "Genre")
    album = find_field(track, "Album")
    length = find_field(track, "Total Time")
    count = find_field(track, "Play Count")
    rating = find_field(track, "Rating")

    if (artist):
        insert_artist = """INSERT INTO Artist(name) SELECT ? WHERE NOT EXISTS 
            (SELECT * FROM Artist WHERE name = ?)"""
        cursor.execute(insert_artist,(artist, artist))

    if (genre): 
        genre_statement = """INSERT INTO Genre(name) SELECT ? WHERE NOT EXISTS 
            (SELECT * FROM Genre WHERE name = ?)"""
        cursor.execute(genre_statement,(genre, genre))

    if (album):
        find_artist_id = "SELECT id from Artist WHERE name = ?"
        cursor.execute(find_artist_id, (artist, ))
        artist_id = cursor.fetchone()[0] 

        insert_album = """INSERT INTO Album(title, artist_id) 
            SELECT ?, ? WHERE NOT EXISTS (SELECT * FROM Album WHERE title = ?)"""
        cursor.execute(insert_album,(album, artist_id, album))

    if (title):
        find_genre_id = "SELECT id from Genre WHERE name = ?"
        cursor.execute(find_genre_id, (genre, ))
        try:
            genre_id = cursor.fetchone()[0]
        except TypeError:
            genre_id = 0
        find_album_id = "SELECT id from Album WHERE title = ?"
        cursor.execute(find_album_id, (album, ))
        try:
            album_id = cursor.fetchone()[0]
        except TypeError:
            album_id = 0
        insert_track = """INSERT INTO Track(title, album_id, genre_id, len,
            rating, count) SELECT ?, ?, ?, ?, ?, ?
                WHERE NOT EXISTS (SELECT * FROM Track WHERE title = ?)"""
        cursor.execute(insert_track, (title, album_id, genre_id, length, rating, count, title))
test1="""SELECT Track.title, Artist.name, Album.title, Genre.name
FROM Track JOIN Album ON Track.album_id = Album.id
	JOIN Genre ON Track.genre_id = Genre.id
	JOIN Artist ON Album.artist_id = Artist.id
ORDER BY Artist.name LIMIT 5;"""
cursor.execute(test1)
print(cursor.fetchall())

test2="""SELECT Track.title, Artist.name, Album.title, Genre.name
FROM Track JOIN Album ON Track.album_id = Album.id
	JOIN Genre ON Track.genre_id = Genre.id
	JOIN Artist ON Album.artist_id = Artist.id
ORDER BY Album.title LIMIT 5;"""
cursor.execute(test2)
print(cursor.fetchall())

test3="""SELECT DISTINCT Artist.name, Track.rating
FROM Track 
  JOIN Album ON Track.album_id = Album.id
	JOIN Artist ON Album.artist_id = Artist.id
  WHERE rating=100
  ORDER BY Artist.name;"""

cursor.execute(test3)


with open('artists_rating_100.txt','w') as f:
  for i in cursor.fetchall():
    tekst=str(i)
    print(tekst)
    f.write(tekst)
    f.write('\n')


conn.commit()
cursor.close()