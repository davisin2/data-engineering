from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
from pyspark.sql.functions import lit

def loadMovieNames():
    movieNames = {}
    with open('u.item') as f:
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1].decode('ascii', 'ignore')
    return movieNames

# For u.data - return (userID, movieId, rating) 
def parseInput(line):
    fields = line.value.split()
    return Row(userID = int(fields[0]), movieID = int(fields[1]), rating = float(fields[2]) )

if __name__=="__main__":
    # Create a SparkSession
    spark = SparkSession.builder.appName("MovieRecs").getOrCreate()

    # load up your movieId -> movieName
    movieNames = loadMovieNames()

    # Get the raw data
    lines = spark.read.text("hdfs://user/maria_dev/ml-100k/u.data").rdd

    #  Convert it to RDD of Row Objects with (userID, movieId, rating)
    ratingsRDD = lines.map(parseInput)

    # convert to Dataframe and cache it
    ratings = spark.createDataFrame(ratingsRDD).cache()

    # create and ALS collaborative filtering model from the complete dataset
    als = ALS(maxIter=5, regParam=0.01, useCol='userID', itemCol='movieID', ratingCol='rating')
    model = als.fit(ratings)

    # Print out ratings for user 0
    print("\nRatings for User ID 0: ")
    userRatings = ratings.filter("userID = 0")
    for rating in userRatings.collect():
        print(movieNames[rating['movieID']], rating['rating'])

    print("\nTop 20 Recommendations: ")
    # Find movies rated more than 100 times
    ratingCounts = ratings.groupBy("movieID").count().filter("count >100")
    # construct a "test" dataframe for user 0 with every movie rated more than 100 times
    popularMovies = ratingCounts.select('movieID').withColumn('userID', lit(0))

    # Run our model on that list of polular movies for user ID 0
    recommendations = model.transform(popularMovies)

    #  Get the top 20 movies with the highest predicted rating for this user
    topRecommendations  = recommendations.sort(recommendations.prediction.desc()).take(20)

    for recommendation in topRecommendations:
        print(movieNames[recommendation['movieID']], recommendation['prediction'])

    spark.stop()