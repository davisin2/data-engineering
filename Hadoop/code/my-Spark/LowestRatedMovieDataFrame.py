from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions

def loadMovieNames():
    movieNames = {}
    with open('u.item') as f:
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1]
    return movieNames

# For u.data - return (movieId, rating) 
def parseInput(line):
    fields = line.split()
    return Row(movieID = int(fields[1]), rating = float(fields[2]) )

if __name__=="__main__":
    # Create a SparkSession
    spark = SparkSession.builder.appName("PopularMovies").getOrCreate()

    # load up your movieId -> movieName
    movieNames = loadMovieNames()

    # Get the raw data
    lines = spark.sparkContext.textFile("hdfs://user/maria_dev/ml-100k/u.data")

    #  Convert it to RDD of Row Objects with (movieId, rating)
    movies = lines.map(parseInput)

    # convert that to Dataframe
    movieDataset = spark.createDataFrame(movies)

    # Compute average rating for each movie ID
    averageRating = movieDataset.groupBy("movieID").avg("rating")

    # Compute Count of ratings for each movieID
    counts = movieDataset.groupBy("movieID").count()

    # Join the two together (we now have movieID, avg(rating) and count columns)
    averagesAndCounts = counts.join(averageRating, "movieID")

    # pull the top 10 results
    topTen = averagesAndCounts.orderBy("avg(rating)").take(10)

    # Print them out, converting movieIDs to names as we go
    for movie in topTen: 
        print(movieNames[movie[0]], movie[1], movie[2])

    # Stop the session
    spark.stop()