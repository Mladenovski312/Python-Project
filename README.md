# Python-Project
Musical Database
Musical track database

Mini application is to read the XML file
Library.xml, and to produce a normalized database.

Artists with rating equal to 100 alphabetically ordered 
should be written in a text file called artists_rating_100.txt.

Statement to get the information from the database is:

How to test your solution:

Test 1.

SELECT Track.title, Artist.name, Album.title, Genre.name
FROM Track JOIN Album ON Track.album_id = Album.id
	JOIN Genre ON Track.genre_id = Genre.id
	JOIN Artist ON Album.artist_id = Artist.id
ORDER BY Artist.name LIMIT 5

The expected result of Test 1. query on your database is:

"For Those About To Rock (We Salute You)"	"AC/DC"	"Who Made Who"	"Rock"
"Hells Bells"	"AC/DC"	"Who Made Who"	"Rock"
"Shake Your Foundations"	"AC/DC"	"Who Made Who"	"Rock"
"You Shook Me All Night Long"	"AC/DC"	"Who Made Who"	"Rock"
"Who Made Who"	"AC/DC"	"Who Made Who"	"Rock"


Test 2.

SELECT Track.title, Artist.name, Album.title, Genre.name
FROM Track JOIN Album ON Track.album_id = Album.id
	JOIN Genre ON Track.genre_id = Genre.id
	JOIN Artist ON Album.artist_id = Artist.id
ORDER BY Album.title LIMIT 5

The expected result of Test 2. query on your database is:

"Circles"	"Bryan Lee"	"Blues Is"	"Funk"
"Gelle"	"Bryan Lee"	"Blues Is"	"Blues/R&B"
"I Worry"	"Bryan Lee"	"Blues Is"	"Blues/R&B"
"Its Your Move"	"Bryan Lee"	"Blues Is"	"Blues/R&B"
"Let me Down Easy"	"Bryan Lee"	"Blues Is"	"Blues/R&B"


Test 3.

The produced file artists_rating_100.txt should contain

AC/DC 100 
Billy Price 100 
Black Sabbath 100 
Bryan Lee 100 
Johnny Cash 100 
Led Zeppelin 100 
Pink Floyd 100 
Queen 100 
Rammstein 100 
Rob Dougan 100 
The Canettes Blues Band 100 
The Who 100 
Various 100 

