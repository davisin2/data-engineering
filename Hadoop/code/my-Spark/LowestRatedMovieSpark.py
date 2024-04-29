
from pyspark import SparkConf, SparkContext

def loadMovieNames():
    movieNames = {}
    with open('u.item', encoding='utf-8') as f:
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1]
    return movieNames

# For u.data - return (movieId, (rating,1.0)) 
def parseInput(line):
    fields = line.split()
    return (int(fields[1]), (float(fields[2]), 1.0)  )

if __name__=="__main__":
    conf = SparkConf().setAppName("WorstMovies")
    sc = SparkContext(conf=conf)

    # Lookup Table movieID-> movieName
    movieNames = loadMovieNames()

    lines=sc.textFile("hdfs://user/maria_dev/ml-100k/u.data")
    # lines=sc.textFile("u.data")

    # convert to movieId, (rating,1.0)) 
    movieRatings = lines.map(parseInput)

    # Reduce to (movieId, (sumOfRatings, totalRatings))         ----------------> ?
    ratingTotalsAndCount = movieRatings.reduceByKey(lambda movie1, movie2 : (movie1[0]+movie2[0],  movie1[1]+movie2[1]) )

    # Map to (movieId, avergaeRating)
    averageRatings = ratingTotalsAndCount.mapValues(lambda totalAndCount: totalAndCount[0]/totalAndCount[1])

    # Sort By average Rating
    sortedMovies = averageRatings.sortBy(lambda x: x[1])

    # Take the top 10 results 
    results = sortedMovies.take(10)

    # Print them out
    for result in results:
        print(movieNames[result[0]], result[1])


