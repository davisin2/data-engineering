HDP 2.6.5:
yum-config-manager --save --setopt=HDP-SOLR-2.6-100.skip_if_unavailable=true
yum install https://repo.ius.io/ius-release-el7.rpm https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum install python-pip
pip install pathlib
pip install mrjob==0.7.4
pip install PyYAML==5.4.1
yum install nano
wget http://media.sundog-soft.com/hadoop/RatingsBreakdown.py
wget http://media.sundog-soft.com/hadoop/ml-100k/u.data

This is required for HDP 2.5 :
pip install google-api-python-client==1.6.4

<!-- Update Python to 2.7 before executing last command -->
yum install scl-utils
yum install centos-release-scl
yum install python27
scl enable python27 bash



For HDP 2.5
Cd /etc/yum.repo.d
Cp sandbox.repo /tmp
Rm –rf sandbox.repo
Cd ~
Yum install python-pip
pip install google-api-python-client==1.6.4
pip install mrjob==0.5.11
yum install nano
...



Run locally:
python RatingsBreakdown.py u.data 

Run on Hadoop
python RatingsBreakdown.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar u.data  


python RatingsBreakdown.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar  hdfs:// u.data 


<!-- Install PySpark -->
pip install pyspark
http://media.sundog-soft.com/hadoop/Spark.zip

spark-submit LowestRatedMovieSpark.py


export SPARK_MAJOR_VERSION=2
spark-submit LowestRatedMovieDataFrame.py


<!-- MLLib -->
sudo pip install numpy==1.16
export SPARK_MAJOR_VERSION=2
spark-submit MovieRecommendationsALS.py


executing hive files
hive -f /path/queries.hql

<!-- -------------------Sqoop ------------------------ -->
For Hadoop 2.6.5

su root
systemctl stop mysqld
systemctl set-environment MYSQLD_OPTS="--skip-grant-tables --skip-networking"
systemctl start mysqld
mysql -uroot
------- Mysql cmd 
FLUSH PRIVILEGES;
alter user 'root'@'localhost' IDENTIFIED BY 'hadoop';
FLUSH PRIVILEGES;
QUIT;
------ CMD
systemctl unset-environment MYSQLD_OPTS
systemctl restart mysqld

mysql -uroot -phadoop

<!-- Inside Database -->
CREATE DATABASE movielens;
SHOW DATABASES;

wget http://media.sundog-soft.com/hadoop/movielens.sql

SET NAMES 'utf8';
SET CHARACTER SET utf8;
USE movielens;

source movielens.sql;
SHOW TABLES;

select * from movies limit 10;

describe ratings;
SELECT movies.title, COUNT(ratings.movie_id) AS ratingCount 
FROM movies
INNER JOIN ratings
ON movies.id == ratings.movie_id
GROUP BY movies.title
ORDER BY ratingCount;

EXIT;
----- SQL Setup complete
mysql -uroot -phadoop

GRANT ALL PRIVILEGES on movielens.* TO root@localhost IDENTIFIED BY 'hadoop';
exit;

<!-- Import in HDFS -->
sqoop import --connect jdbc:mysql://localhost/movielens --driver com.mysql.jdbc.Driver --table movies -m 1 --username root --password hadoop

<!-- Import in Hive -->
sqoop import --connect jdbc:mysql://localhost/movielens --driver com.mysql.jdbc.Driver --table movies -m 1 --username root --password hadoop --hive-import

<!-- Export Data from Hadoop to MySQL -->
Table should exist
mysql -uroot -phadoop
use movielens;

CREATE TABLE exported_movies (
    id INT,
    title VARCHHAR(255),
    releaseData DATE
);
EXIT;

/apps/hive/warhouse/movies/

sqoop export --connect jdbc:mysql://localhost/movielens -m 1 --driver com.mysql.jdbc.Driver --table exported_movies  --export-dir /apps/hive/warhouse/movies --input-fields-terminated-by '\001' --username root --password hadoop

mysql -uroot -phadoop
SELECT * FROM exported_movies LIMIT 10;
exit;


<!-- Start REST SERVICE for HBase -->
su root
/usr/hdp/current/hbase-master/bin/hbase-daemon.sh start rest -p 8000 --infoport 8001

pip install starbase

/usr/hdp/current/hbase-master/bin/hbase-daemon.sh stop rest

<!-- HBase with PIG -->
1. Upload u.user to /usr/maria_dev/ml-100k on HDFS using File View
2. Create Table in Habse
Putty -> su root ->
hbase shell
list
create 'users', 'userinfo'
<!-- userinfo -> column family -->
list
exit

wget http://media.sundog-soft.com/hadoop/hbase.pig
root@ ...maria_dev # pig hbase.pig

maria_dev # hbase shell
> list
> scan 'users'
> disable 'users'
> drop 'users'
> list

exit
exit

Service -> Hbase -> Stop



<!-- Cassandra -->
cassandra requires python 2.7, centos (HDP) requires python 2.6

1. Open Putty session to HDP
2. su root
# yum install scl-utils
# yum install centos-release-scl-rh
# yum install python27
#  scl enable python27 bash
# python -V
# cd /etc/yum.repos.d/
# vi datastax.repo
[datastax]
name = Datastax repo for apache Cassandra
baseurl = http://rpm.datastax.com/community
enabled = 1
gpgcheck = 0

# cat datastax.repo
# yum install dsc30
# service cassandra start
# cqlsh
# cqlsh --cqlversion="3.4.0" (if error)

> CREATE keyspace movielens WITH replication = {'Class': 'SimpleStrategy' , replication_factor: '1'} AND durable_writes = true;
> USE movielens;
> CREATE TABLE users (user_id int, age int, gender text, occupation text, zip text, PRIMARY KEY (user_id));
> DESCRIBE TABLE users;
> SELECT * FROM users;

<!-- [Activity] Write Spark Output into Cassandra -->

> exit
# wget http://media.sundog-soft.com/hadoop/CassandraSpark.py
# export SPARK_MAJOR_VERSION=2
# spark-submit --packages datastax:spark-cassandra-connector:2.0.0-M2-s_2.11 CassandraSpark.py
<!-- Spark 2.0.0 Scala 2.11  -->
#  On HDP 2.6.5
# spark-submit --packages datastax:spark-cassandra-connector_2.11:2.4.2 CassandraSpark.py

# cqlsh --cqlversion="3.4.0"
> USE movielens;
> SELECT * FROM users LIMIT 10;
> exit
# service cassandra stop



<!-- MongoDB -->
# su root
# cd /var/lib/ambari-server/resources/stacks
# ls
# cd HDP
# ls
# cd 2.5/services
# pwd
# git clone https://github.com/nikunjness/mongo-ambari.git  
# sudo service ambari restart
# 
127.0.0.1:8080
admin


Actions-> Add Service -> Select Mongo DB -> next... -> Deploy

# pip install pymongo==3.4.0
# 

$ cd ~
$ wget http://media.sundog-soft.com/hadoop/MongoSpark.py
$ cat MongoSpark.py
$ export SPARK_MAJOR_VERSION=2
$ spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.0.0 MongoSpark.py


HDP 2.6.5
$ spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.3.2 MongoSpark.py

# export LC_ALL= C
# mongo
> use movielens;
> db.users.find({user_id:100});
> db.users.explain().find({user_id:100});
> db.users.createIndex({user_id:1});  # 1 means ASCENDING
> db.users.explain().find({user_id:100});
> db.users.find({user_id:100});

<!-- Mongo DB doesn't set  Index for you, we have to set it -->

> db.users.aggregate([
     { $group: {_id: {occupation: "$occupation}, avgAge: {$avg: "$age} } }
])

> db.users.count()
> db.getCollectionInfos()
> db.users.drop()
> db.getCollectionInfos()
> exit

# Ambari -> Services -> MongoDB -> Stop

<!-- Drill -->
1. Login to Ambari (admin)
2. Start MongoDB Service
3. Hive view

 CREATE DATABASE movielens;

 4. Upload Table (ratings)
 CSV, Delimited 9 Tab
user_id, movie_id, rating, epoch_seconds


-- Insert Data in MongoDB
1. login using putty
2. su root


# export SPARK_MAJOR_VERSION=2
# spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.0.0 MongoSpark.py

HDP 2.6.5
# spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.3.2 MongoSpark.py


-- Install Drill
# wget http://archive.apache.org/dist/drill/drill-1.12.0/apache-drill-1.12.0.tar.gz
# tar -xvf apache-drill-1.12.0.tar.gz
# cd apache-drill-1.12.0
# bin/drillbit.sh start -Ddrill.exec.port=8765
# 

Go to 127.0.0.1:8765

1. Storage -> cp, dfs, hive, mongo
2. hive -> Update
hive.metastore.uris = "thrift://localhost:9083"
Update


3. Query

SHOW DATABASES;

__ hive.movielens
__ mongo.movielens

SELECT * FROM hive.movielens.ratings LIMIT 10;

SELECT * FROM mongo.movielens.users LIMIT 10;


SELECT u.occupations, COUNT(*)
FROM hive.movielens.ratings r
JOIN mongo.movielens.users u
ON r.user_id = u.user_id
GROUP BY u.occupations;

# bin/drillbit.sh stop
- Stop MongoDB from Ambari


<!-- Phoenix -->
1. Ambari (127.0.0.1:8080 - admin) -> HBase -> Start
2. Login using ssh
 su root
# cd /usr/hdp/current/phoenix-client/
2.6.5 Phoenix is already installed
# cd bin
# python sqlline.py
> !tables;
> CREATE TABLE IF NOT EXISTS us_population ( state CHAR(2) NOT NULL, city VARCHAR NOT NULL, population BIGINT 
CONSTRAINT my_pk PRIMARY KEY (state,city)
);
> !tables;
> UPSERT INTO us_population VALUES('NY', 'New York', 8143197);
> UPSERT INTO us_population VALUES('CA', 'Los Angles', 3844829);
> SELECT * FORM us_population;
> SELECT * FORM us_population WHERE state='CA';
> DROP TABLE us_population;
> !tables
> !quit

<!-- PIG script which use phoenix to write/store users Data Table, and read back  -->
# cd /usr/hdp/current/phoenix-client/bin
# python sqlline.py
>  CREATE TABLE IF NOT EXISTS users ( USERID INTEGER NOT NULL, age INTEGER , GENDER CHAR(1), OCCUPATION VARCHAR, ZIP VARCHAR 
CONSTRAINT pk PRIMARY KEY (USERID)
);
> !tables
> !quit 
# cd /home/maria_dev
# mkdir ml-100k
# wget http://media.sundog-soft.com/hadoop/ml-100k/u.user
# cd /home/maria_dev
# wget http://media.sundog-soft.com/hadoop/phoenix.pig
# cat phoenix.pig
# pig phoenix.pig
# cd /usr/hdp/current/phoenix-client/bin
# python sqlline.py

> !tables
> SELECT * FROM users LIMIT 10;
> DROP TABLE users;
> !tables
> !quit

- Shut down HBase

<!-- Presto -->

<!-- [Activity] Install Presto and query Hive with it -->
https://prestodb.io/docs/0.286/installation/deployment.html

su root
/home/maria_dev
# wget https://repo1.maven.org/maven2/com/facebook/presto/presto-server/0.286/presto-server-0.286.tar.gz
(URL from prestodb.io -> Docs -> Installation -> Deploying Presto)

# tar -xvf presto-server-0.286.tar.gz
# cd presto-server-0.286
# wget http://media.sundog-soft.com/hadoop/presto-hdp-config.tgz
# tar -xvf presto-hdp-config.tgz

<!-- Install Presto CLI -->
https://prestodb.io/docs/0.286/installation/cli.html
# cd /home/maria_dev/presto-server-0.286/bin
# wget https://repo1.maven.org/maven2/com/facebook/presto/presto-cli/0.286/presto-cli-0.286-executable.jar
# mv presto-cli-0.286-executable.jar presto
# chmod +x presto
# cd ..
# pwd
/home/maria_dev/presto-server-0.286/
# bin/launcher start

127.0.0.1:8090

<!-- Hiove should have ratings table -->
# bin/presto --server 127.0.0.1:8090 --catalog hive
presto> show tables from default
> SELECT * from default.ratings LIMIT 10;
> SELECT * from default.ratings  WHERE rating=5 LIMIT 10;
> SELECT count(*) from default.ratings  WHERE rating=1;
> quit

# bin/launcher stop

<!-- [Activity] Query both Cassandra and Hive using Presto  -->

# scl enable python27 bash
# python -V
# service cassandra start
# nodetool enablethrift
# cqlsh --cqlversion="3.4.0"
> DESCRIBE KEYSPACES;
> use moveilens;
> descirbe tables
> select * from users limit 10;
> quit

# cd /home/maria_dev/presto-server-0.286/etc/catalog/
# vi cassandra.properties
connector.name=cassandra
cassandra.contact-points=127.0.0.1
# cd ../..
# bin/launcher start
# bin/presto --server 127.0.0.1:8090 --catalog hive,cassandra
> show tables from cassandra.movielens;
> describe cassandra.movielens.users;
> select * from cassandra.movielens.users limit 10;
> select * from hive.default.ratings limit 10;
> select u.occupation, count(*) 
FROM hive.default.ratings r 
JOIN cassandra.movielens.users u
ON r.user_id = u.user_id
GROUP BY u.occupation;

> quit
# bin/launcher stop
# service cassandra stop


<!-- [Activity] Use Hive on Tez and measure the performance benefits -->
1. Ambari (127.0.0.1:8080 - admin)
2. Hive View
Database: movielens
Table: rating (user_id, movie_id, rating, epoch_seconds)

Table: names
upload u.item file (Delimited |)
movie_id, name, release_date,


Query:

DROP VIEW IF EXISTS topMovieIDs;

CREATE VIEW topMovieIDs AS
SELECT movieID, count(movieID) AS ratingCount
FROM movielens.rating
GROUP BY movie_id
ORDER BY ratingCount DESC;

SELECT n.name, ratingCount
FROM topMovieIDs t 
JOIN movielens.names n
ON t.movie_id = n.movie_id;


Settings -> Add -> hive.execution.engine, tex/mr

<!-- [Activity] Simulating a failing master with ZooKeeper -->
1. login using ssh
2. su root
# cd /usr/hdp/current/zookeeper-current/bin
# ls
..
zkCli.sh
# ./zkCli.sh 
ls /
create -e /testmaster "127.0.0.1:2223"
<ephermaral node>
get /testmaster
quit

# ./zkCli.sh 
ls /
<automatically deleted testmaster>
get /testmaster
<Node doesn't exist>
create -e /testmaster "127.0.0.1:2225"
get /testmaster
create -e /testmaster "127.0.0.1:2225"
<Node Already exists>
quit

#
- Ideally, we should zookeeper client in Java

<!-- [Activity] Setup a simple Oozie workflow -->

login using ssh
1. sqoop extratc from MySQL
2. Use HIVE to analyse the data

# mysql -u root -p
hadoop
> show databases;
> quit

# wget http://media.sundog-soft.com/hadoop/movielens.sql
# mysql -u root -p
hadoop

> SET NAMES 'utf8';
> SET CHARACTER SET utf8;
> CREATE DATABASE movielens;
> SHOW DATABASES;
> USE movielens;
> source movielens.sql;
> SHOW TABLES;
> select * from movies limit 10;
> GRANT ALL PRIVILEGES ON movielens.* TO ''@'localhost';

On HDP 2.6.5, use
GRANT ALL ON movielens.* TO 'root'@'localhost' IDENTIFIED BY 'hadoop';
instead

> quit

# wget http://media.sundog-soft.com/hadoop/oldmovies.sql
# wget http://media.sundog-soft.com/hadoop/workflow.xml
# wget http://media.sundog-soft.com/hadoop/job.properties
<this is for HDP 2.6.5>
<for 2.5.0 job.properties
nameNode=hdfs://sandbox.hortonworks.com:8020
jobTracker=http://sandbox.hortonworks.com:8050
queueName=default 
oozie.use.system.libpath=true
oozie.wf.application.path=${nameNode}/user/maria_dev
>
<!-- upload workflow.xml to hadoop  -->

# hadoop fs -put workflow.xml /user/maria_dev
# hadoop fs -put oldmovies.sql /user.maria_dev

<!-- for sqoop to connect to mysql, we need to install mysql connector -->

# hadoop fs -put /usr/share/java/mysql-connector-java.jar /user/oozie/share/lib/lib_*/sqoop
* - ambari, go to File view -> /user/oozie/share/lib/ -> copy folder and replace *

<!-- restart oozie -->
Amabari -> Services -> Oozie -> Restart All

# oozie job -oozie http://localhost:11000/oozie -config /home/maria_dev/job.properties -run

Go to http://localhost:11000/oozie 

# exit

<!--  [Activity] Use Zappeline to analyse movie ratings Part 1,2-->
Zappeline is pre- installed on HDP
Go to http://localhost:9995

create new Note
Interpreter binding -> Sparkl should be on top

http://media.sundog-soft.com/hadoop/MovieLens.json
Zappeline -> Import MovieLens.json

gethue.com

