from starbase import Connection
# starbase - Python Client for HBase with Python wrappr on top of it

c = Connection("127.0.0.1", "8000")

ratings = c.table('ratings')

if ratings.exists():
    print("Dropping existing ratings table\n")
    ratings.drop()

# creating column family
ratings.create('ratings')

print("Parsing the ml-100k ratings data...\n")
ratingsFile = open("e:/Downloads/ml-100k/ml-100k/u.data", "r")

batch = ratings.batch()

for line in ratingsFile:
    (userID, movieID, rating, timestamp) = line.split()
    batch.update(userID, {'rating' : {movieID: rating}})

ratingsFile.close()

print("Commiting rating data into HBase via REST Service\n")
batch.commit(finalize=True)

print("Get back ratings for some users...\n")
print("Rating for USer ID 1: \n")
print(ratings.fetch("1"))

print("Rating for USer ID 33: \n")
print(ratings.fetch("33"))

ratings.drop()