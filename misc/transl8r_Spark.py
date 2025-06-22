#===============================================================================
#-------------------------------------------------------------------------------
"""\
val file = spark.textFile("hdfs://...");
val errs = file.filter(line => line.contains("ERROR"));
val ones = errs.map(item => 1);
val count = ones.reduce(total, count => total + count);

val file = spark.textFile("hdfs://...");
val errs = file.filter(line => line.contains("ERROR"));
val cachedErrs = errs.cache();
val ones = cachedErrs.map(item => 1);
val count = ones.reduce(total, count => total + count);

// Read points from a text file and cache them
val points = spark.textFile("...").map(parsePoint).cache();
// Initialize w to random D-dimensional vector
var w = Vector.random(D);
// Run multiple iterations to update w
for (i <- 1 to ITERATIONS) {
    val grad = spark.accumulator(new Vector(D));
    for (p <- points) { // Runs in parallel
        val s = (1/(1+exp(-p.y*(w dot p.x)))-1)*p.y;
        grad += s * p.x;
    }
    w -= grad.value;
}

val Rb = spark.broadcast(R);
for (i <- 1 to ITERATIONS) {
    U = spark.parallelize(0 until u).map(j => updateUser(j, Rb, M)).collect();
    M = spark.parallelize(0 until m).map(j => updateUser(j, Rb, U)).collect();
}

lines = spark.textFile("hdfs://...");
errors = lines.filter(line => line.startsWith("ERROR"));
errors.persist();
errors.count();
//------------------------------------------------------------------------------
// Count errors mentioning MySQL:
errors.filter(line => line.contains("MySQL")).count()
// Return the time fields of errors mentioning
// HDFS as an array (assuming time is field
// number 3 in a tab-separated format):
errors.filter(line => line.contains("HDFS")).map(line => line.split('\t')[3]).collect()
//------------------------------------------------------------------------------
val points = spark.textFile("...").map(parsePoint).persist();
var w = 0; // random initial vector
for (i <- 1 to ITERATIONS) {
    val gradient = points.map( p =>
        p.x * (1/(1+exp(-p.y*(w dot p.x)))-1)*p.y
    ).reduce((a,b) => a+b);
    w -= gradient;
}
//------------------------------------------------------------------------------
// Load graph as an RDD of (URL, outlinks) pairs
val links = spark.textFile(...).map(...).persist()
var ranks = // RDD of (URL, rank) pairs
for (i <- 1 to ITERATIONS) {
    // Build an RDD of (targetURL, float) pairs
    // with the contributions sent by each page
    val contribs = links.join(ranks).flatMap {
        (url, (links, rank)) =>
        links.map(dest => (dest, rank/links.size))
    }
    // Sum contributions by URL and get new ranks
    ranks = contribs.reduceByKey((x,y) => x+y).mapValues(sum => a/N + (1-a)*sum)
}
links = spark.textFile("...").map("...").partitionBy(myPartFunc).persist()
//------------------------------------------------------------------------------
"""