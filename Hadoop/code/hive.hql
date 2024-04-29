

CREATE VIEW IF NOT EXISTS topMovieIDs AS  
SELECT movieID, count(movieID) as ratingCount
FROM ratings
GROUP BY movieID
ORDER BY ratingCount DESC;


SELECT * FROM topMovieIDs;

SELECT n.title, ratingCount
FROM topMovieIDs t 
JOIN names n ON
t.movieID == n.movieID;

DROP VIEW topMovieIDs;


-- Challenge
CREATE VIEW IF NOT EXISTS avgRatings AS
SELECT movieID, AVG(rating) as avgRating, COUNT(rating) as ratingCount
FROM ratings
GROUP BY movieID
-- HAVING COUNT(rating) >10
ORDER BY AVG(rating) DESC
-- LIMIT 1;

SELECT n.title, avgRating
FROM avgRatings t JOIN names n
ON t.movieID == n.movieID
WHERE ratingCount>10;
