#===================================================================================================
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
GLOBALS(globals())
TRACE(40)
#---------------------------------------------------------------------------------------------------
def init_list(v): return λ(f"{v} = None; stack = []")
def push_list(v): return λ(f"stack.append([{v}])")
def push_item(v): return λ(f"stack[-1].append({v})")
def pop_list():   return λ(f"stack[-2].append(tuple(stack.pop()))")
def pop_final(v): return λ(f"{v} = tuple(stack.pop())")
#===================================================================================================
η               = FENCE(SPAN(' \t\r\n') | ε())
def ς(s):       return η + ς(s)
#---------------------------------------------------------------------------------------------------
identifier      = ANY(UCASE+LCASE) + FENCE(SPAN(DIGITS+UCASE+'_'+LCASE) | ε())
variable        = η + identifier % "tx"
_True           = variable + Λ(lambda: tx == "True")
_False          = variable + Λ(lambda: tx == "False")
_lambda         = variable + Λ(lambda: tx == "lambda")
_reduce         = variable + Λ(lambda: tx == "reduce")
_collect        = variable + Λ(lambda: tx == "collect")
_foreach        = variable + Λ(lambda: tx == "foreach")
_parallelize    = variable + Λ(lambda: tx == "parallelize")
_val            = variable + Λ(lambda: tx == "val")
_var            = variable + Λ(lambda: tx == "var")
#---------------------------------------------------------------------------------------------------
_map            = variable + Λ(lambda: tx == "map")
_filter         = variable + Λ(lambda: tx == "filter")
_flatMap        = variable + Λ(lambda: tx == "flatMap")
_sample         = variable + Λ(lambda: tx == "sample")
_groupByKey     = variable + Λ(lambda: tx == "groupByKey")
_union          = variable + Λ(lambda: tx == "union")
_join           = variable + Λ(lambda: tx == "join")
_cogroup        = variable + Λ(lambda: tx == "cogroup")
_crossProduct   = variable + Λ(lambda: tx == "crossProduct")
_mapValues      = variable + Λ(lambda: tx == "mapValues")
_crossProduct   = variable + Λ(lambda: tx == "crossProduct")
_partitionBy    = variable + Λ(lambda: tx == "partitionBy")
_count          = variable + Λ(lambda: tx == "count")
_collect        = variable + Λ(lambda: tx == "collect")
_reduceByKey    = variable + Λ(lambda: tx == "reduceByKey")
_lookup         = variable + Λ(lambda: tx == "lookup")
_save           = variable + Λ(lambda: tx == "save")
#---------------------------------------------------------------------------------------------------
number          = η + (SPAN("0123456789")) % "tx"
boolean         = η + (_True | _False) % "tx"
string          = η + (σ('"') + BREAK('"') + σ('"')) % "tx"
#---------------------------------------------------------------------------------------------------
function        = η +   ( _map            + σ('(') + σ(')')
                        | _filter         + σ('(') + σ(')')
                        | _flatMap        + σ('(') + σ(')')
                        | _sample         + σ('(') + σ(')')
                        | _groupByKey     + σ('(') + σ(')')
                        | _union          + σ('(') + σ(')')
                        | _join           + σ('(') + σ(')')
                        | _cogroup        + σ('(') + σ(')')
                        | _crossProduct   + σ('(') + σ(')')
                        | _mapValues      + σ('(') + σ(')')
                        | _crossProduct   + σ('(') + σ(')')
                        | _partitionBy    + σ('(') + σ(')')
                        | _count          + σ('(') + σ(')')
                        | _collect        + σ('(') + σ(')')
                        | _reduceByKey    + σ('(') + σ(')')
                        | _lookup         + σ('(') + σ(')')
                        | _save           + σ('(') + σ(')')
                        )
#---------------------------------------------------------------------------------------------------
element         = ς('_') | variable | number | boolean | string
elements        = element + (ς(',') + ζ(lambda: elements) | ε())
collection      = ς('[') + elements + ς(']')
parameters      = (identifier + (ς(',') + ζ(lambda: parameters) | ε()))
xlambda         = _lambda + parameters + ς(':') + ζ(lambda: expression)
factor          = ( element
                  | identifier
                  | ς('(') + ζ(lambda: expression) + ς(')')
                  )
term            = ( factor
                  + ( ς('*') + ζ(lambda: term)
                    | ς('/') + ζ(lambda: term)
                    | ε()
                    )
                  )
expression      = ( term
                  + ( ς('+')+ ζ(lambda: expression)
                    | ς('-')+ ζ(lambda: expression)
                    | ε()
                    )
                  )
assignment      = ς('val') + identifier + ς('=') + ζ(lambda: expression)
creation        = ς('from_a_file') + ς('(') + string + ς(')')
                | ς('parallelize') + ς('(') + collection + ς(')')
transformation  = identifier + ς('.') + ς('transforming')               + ς('(') + xlambda + ς(')')
                | identifier + ς('.') + ς('changing_the_persistence')   + ς('(') + boolean + ς(')')
action          = identifier + ς('.') + ς('reduce')                     + ς('(') + xlambda + ς(')')
                | identifier + ς('.') + ς('collect')                    + ς('(') + ς(')')
                | identifier + ς('.') + ς('foreach')                    + ς('(') + xlambda + ς(')')
statement       = assignment
#               | creation
#               | transformation
#               | action
statements      = ARBNO(statement + ς(';'))
program         = POS(0) statements RPOS(0)
#===================================================================================================
"""\
    val file = spark.textFile("hdfs://...");
    val errs = file.filter(_.contains("ERROR"));
    val ones = errs.map(_ => 1);
    val count = ones.reduce(_ + _);
    val cachedErrs = errs.cache();
    val points = spark.textFile(...).map(parsePoint).cache(); // Read points from a text file and cache them

    var w = Vector.random(D); // Initialize w to random D-dimensional vector
    for (i <- 1 to ITERATIONS) { // Run multiple iterations to update w
        val grad = spark.accumulator(new Vector(D));
        for (p <- points) { // Runs in parallel
            val s = (1 / (1 + exp(-p.y * (w dot p.x))) - 1) * p.y;
            grad += s * p.x;
        }
        w -= grad.value;
    }

    val Rb = spark.broadcast(R);
    for (i <- 1 to ITERATIONS) {
        U = spark.parallelize(0 until u)
            .map(j => updateUser(j, Rb, M))
            .collect();
        M = spark.parallelize(0 until m)
            .map(j => updateUser(j, Rb, U))
            .collect();
    }
"""
#===================================================================================================
def map():          pass # (f: T => U)           : # RDD[T] => RDD[U]
def filter():       pass # (f: T => Bool)        : # RDD[T] => RDD[T]
def flatMap():      pass # (f: T => Seq[U])      : # RDD[T] => RDD[U]
def sample():       pass # (fraction: Float)     : # RDD[T] => RDD[T] # (Deterministic sampling)
def groupByKey():   pass # ()                    : # RDD[(K, V)] => RDD[(K, Seq[V])]
def reduceByKey():  pass # (f: (V, V) => V)      : # RDD[(K, V)] => RDD[(K, V)]
def union():        pass # ()                    : # (RDD[T], RDD[T]) => RDD[T]
def join():         pass # ()                    : # (RDD[(K, V)], RDD[(K, W)]) => RDD[(K, (V, W))]
def cogroup():      pass # ()                    : # (RDD[(K, V)], RDD[(K, W)]) => RDD[(K, (Seq[V], Seq[W]))]
def crossProduct(): pass # ()                    : # (RDD[T], RDD[U]) => RDD[(T, U)]
def mapValues():    pass # (f: V) =>             : # RDD[(K, V)] => RDD[(K, W)] (Preserves partitioning)
def sort():         pass # (c: Comparator[K])    : # RDD[(K, V)] => RDD[(K, V)]
def partitionBy():  pass # (p: Partitioner[K])   : # RDD[(K, V)] => RDD[(K, V)]
#---------------------------------------------------------------------------------------------------
def count():        pass # ()                    : # RDD[T] => Long
def collect():      pass # ()                    : # RDD[T] => Seq[T]
def reduce():       pass # (f: (T, T) => T)      : # RDD[T] => T
def lookup():       pass # (k: K)                : # RDD[(K, V)] => Seq[V] # (On hash/range partitioned RDDs)
def save():         pass # (path: String)        : # Outputs RDD to a storage system, e.g., HDFS
#===================================================================================================
# §2: Resilient Distributed Datasets (RDDs)
# §2(i): This section provides an overview of RDDs.
# §2(ii): We first define RDDs (§2.1) and introduce their programming interface in Spark (§2.2).
# §2(iii): We then compare RDDs with finer-grained shared memory abstractions (§2.3).
# §2(iv): Finally, we discuss limitations of the RDD model (§2.4).
#---------------------------------------------------------------------------------------------------
# §2.1: RDD Abstraction
# §2.1(i): Formally, an RDD is a read-only, partitioned collection of records.
# §2.1(ii): RDDs can only be created through deterministic operations on either ...
# §2.1(ii): ... (1) data in stable storage or (2) other RDDs.
# §2.1(iii): We call these operations transformations ...
# §2.1(iii): ... to differentiate them from other operations on RDDs.
# §2.1(iv): Examples of transformations include map, filter, and join.
# §2.1(v): RDDs do not need to be materialized at all times.
# §2.1(vi): Instead, an RDD has enough information about how it was derived from other datasets ...
# §2.1(vi): ... (its lineage) to compute its partitions from data in stable storage.
# §2.1(vii): This is a powerful property: in essence, a program ...
# §2.1(vii): ... cannot reference an RDD that it cannot reconstruct after a failure.
# §2.1(viii): Finally, users can control two other aspects of RDDs: persistence and partitioning.
# §2.1(ix): Users can indicate which RDDs they will reuse ...
# §2.1(ix): ... and choose a storage strategy for them (e.g., in-memory storage).
# §2.1(x): They can also ask that an RDD’s elements be partitioned ...
# §2.1(x): ... across machines based on a key in each record.
# §2.1(xi): This is useful for placement optimizations, such as ensuring that ...
# §2.1(xi): ... two datasets that will be joined together are hash-partitioned in the same way.
#===================================================================================================
# §2.2: Spark Programming Interface
#---------------------------------------------------------------------------------------------------
# §2.2.0.1(i): Spark exposes RDDs through a language-integrated API similar to DryadLINQ [31] ...
# §2.2.0.1(i): ... and FlumeJava [8], where each dataset is represented as an object ...
# §2.2.0.1(i): ... and transformations are invoked using methods on these objects.
#---------------------------------------------------------------------------------------------------
# §2.2.0.2(i): Programmers start by defining one or more RDDs through transformations on data ...
# §2.2.0.2(i): ... in stable storage (e.g., map and filter).
# §2.2.0.2(ii): They can then use these RDDs in actions, which are operations that return a value to the application or export data to a storage system.
# §2.2.0.2(iii): Examples of actions include count (which returns the number of elements in the dataset), collect (which returns the elements themselves), and save (which outputs the dataset to a storage system).
# §2.2.0.2(iv): Like DryadLINQ, Spark computes RDDs lazily the first time they are used in an action, so that it can pipeline transformations.
#---------------------------------------------------------------------------------------------------
# §2.2.0.3(i): In addition, programmers can call a persist method to indicate which RDDs they want to reuse in future operations.
# §2.2.0.3(ii): Spark keeps persistent RDDs in memory by default, but it can spill them to disk if there is not enough RAM.
# §2.2.0.3(iii): Users can also request other persistence strategies, such as storing the RDD only on disk or replicating it across machines, through flags to persist.
# §2.2.0.3(iv): Finally, users can set a persistence priority on each RDD to specify which in-memory data should spill to disk first.
#---------------------------------------------------------------------------------------------------
# §2.2.1: Example: Console Log Mining
#---------------------------------------------------------------------------------------------------
# §2.2.1.1(i):   Suppose that a web service is experiencing errors and an operator wants to search terabytes of logs in the Hadoop filesystem (HDFS) to find the cause.
# §2.2.1.1(ii):  Using Spark, the operator can load just the error messages from the logs into RAM across a set of nodes and query them interactively.
# §2.2.1.1(iii): She would first type the following Scala code:
# §2.2.1.1(iv):  Line 1 defines an RDD backed by an HDFS file (as a collection of lines of text), while line 2 derives a filtered RDD from it.
# §2.2.1.1(v):   Line 3 then asks for errors to persist in memory so that it can be shared across queries.
# §2.2.1.1(vi):  Note that the argument to filter is Scala syntax for a closure.
"""\
    lines = spark.textFile("hdfs://..."); // Line 1
    errors = lines.filter(_.startsWith("ERROR")); // Line 2
    errors.persist(); // Line 3
"""
#---------------------------------------------------------------------------------------------------
# §2.2.1.2(i): At this point, no work has been performed on the cluster.
# §2.2.1.2(ii): However, the user can now use the RDD in actions, e.g., to count the number of messages.
"""\
    errors.count();
"""
#---------------------------------------------------------------------------------------------------
# §2.2.1.3(i): The user can also perform further transformations on the RDD and use their results, as in the following lines ...
"""\
    // Count errors mentioning MySQL:
    errors.filter(_.contains("MySQL")).count();
    // Return the time fields of errors mentioning
    // HDFS as an array (assuming time is field
    // number 3 in a tab-separated format):
    errors.filter(_.contains("HDFS"))
          .map(_.split('\t')(3))
          .collect();
"""
#---------------------------------------------------------------------------------------------------
# §2.2.1.4(i): After the first action involving errors runs, Spark will store the partitions of errors in memory, greatly speeding up subsequent computations on it.
# §2.2.1.4(ii): Note that the base RDD, lines, is not loaded into RAM.
# §2.2.1.4(iii): This is desirable because the error messages might only be a small fraction of the data (small enough to fit into memory).
#===================================================================================================
# §3: Spark Programming Interface
#---------------------------------------------------------------------------------------------------
# §3.0.1(i): Spark provides the RDD abstraction through a language-integrated API similar to DryadLINQ [31] in Scala [2], a statically typed functional programming language for the Java VM.
# §3.0.1(ii): We chose Scala due to its combination of conciseness (which is convenient for interactive use) and efficiency (due to static typing).
# §3.0.1(iii): However, nothing about the RDD abstraction requires a functional language.
#---------------------------------------------------------------------------------------------------
# §3.0.2(i): To use Spark, developers write a driver program that connects to a cluster of workers, as shown in Figure 2.
# §3.0.2(ii): The driver defines one or more RDDs and invokes actions on them.
# §3.0.2(iii): Spark code on the driver also tracks the RDDs lineage.
# §3.0.2(iv): The workers are long-lived processes that can store RDD partitions in RAM across operations.
#---------------------------------------------------------------------------------------------------
# §3.0.3(i): As we showed in the log mining example in Section 2.2.1, users provide arguments to RDD operations like map by passing closures (function literals).
# §3.0.3(ii): Scala represents each closure as a Java object, and these objects can be serialized and loaded on another node to pass the closure across the network.
# §3.0.3(iii): Scala also saves any variables bound in the closure as fields in the Java object.
# §3.0.3(iv): For example, one can write code like ...
"""\
    var x = 5; rdd.map(_ + x);
"""
# §3.0.3(iv): ... to add 5 to each element of an RDD.
#---------------------------------------------------------------------------------------------------
# §3.0.4(i): RDDs themselves are statically typed objects parametrized by an element type.
# §3.0.4(ii): For example, RDD[Int] is an RDD of integers.
# §3.0.4(iii): However, most of our examples omit types since Scala supports type inference.
#---------------------------------------------------------------------------------------------------
# §3.0.5(i): Although our method of exposing RDDs in Scala is conceptually simple, we had to work around issues with Scala’s closure objects using reflection [33].
# §3.0.5(ii): We also needed more work to make Spark usable from the Scala interpreter, as we shall discuss in Section 5.2.
# §3.0.5(iii): Nonetheless, we did not have to modify the Scala compiler.
#===================================================================================================
# §3.1 RDD Operations in Spark
#---------------------------------------------------------------------------------------------------
# §3.1.1(i): Table 2 lists the main RDD transformations and actions available in Spark.
# §3.1.1(ii): We give the signature of each operation, showing type parameters in square brackets.
# §3.1.1(iii): Recall that transformations are lazy operations that define a new RDD, while actions launch a computation to return a value to the program or write data to external storage.
#---------------------------------------------------------------------------------------------------
# §3.1.2(i): Note that some operations, such as join, are only available on RDDs of key-value pairs.
# §3.1.2(ii): Also, our function names are chosen to match other APIs in Scala and other functional languages;
# §3.1.2(iii): for example, map is a one-to-one mapping, while flatMap maps each input value to one or more outputs (similar to the map in MapReduce).
#---------------------------------------------------------------------------------------------------
# §3.1.3(i): In addition to these operators, users can ask for an RDD to persist.
# §3.1.3(ii): Furthermore, users can get an RDD’s partition order, which is represented by a Partitioner class, and partition another dataset according to it.
# §3.1.3(iii): Operations such as groupByKey, reduceByKey and sort automatically result in a hash or range partitioned RDD.
#===================================================================================================
# §3.2: Example Applications
#---------------------------------------------------------------------------------------------------
# §3.2.0(i): We complement the data mining example in Section 2.2.1 with two iterative applications: logistic regression and PageRank.
# §3.2.0(ii): The latter also showcases how control of RDDs’ partitioning can improve performance.
#---------------------------------------------------------------------------------------------------
# §3.2.1: Logistic Regression
#---------------------------------------------------------------------------------------------------
# §3.2.1.1(i): Many machine learning algorithms are iterative in nature because they run iterative optimization procedures, such as gradient descent, to maximize a function.
# §3.2.1.1(ii): They can thus run much faster by keeping their data in memory.
#---------------------------------------------------------------------------------------------------
# §3.2.1.2(i): As an example, the following program implements logistic regression [14], a common classification algorithm that searches for a hyperplane w that best separates two sets of points (e.g., spam and non-spam emails).
# §3.2.1.2(ii): The algorithm uses gradient descent: it starts w at a random value, and on each iteration, it sums a function of w over the data to move w in a direction that improves it ...
"""\
    val points = spark.textFile("...").map(parsePoint).persist();
    var w = ???; // random initial vector
    for (i <- 1 to ITERATIONS) {
        val gradient = points.map (
            p => p.x * (1 / (1 + exp(-p.y * (w dot p.x))) - 1) * p.y
        ).reduce((a,b) => a + b);
        w -= gradient;
    }
"""
#---------------------------------------------------------------------------------------------------
# §3.2.1.3(i): We start by defining a persistent RDD called points as the result of a map transformation on a text file that parses each line of text into a Point object.
# §3.2.1.3(ii): We then repeatedly run map and reduce on points to compute the gradient at each step by summing a function of the current w.
# §3.2.1.3(iii): Keeping points in memory across iterations can yield a 20x speedup, as we show in Section 6.1.
#---------------------------------------------------------------------------------------------------
# §3.2.2: PageRank
#---------------------------------------------------------------------------------------------------
# §3.2.2.1(i): A more complex pattern of data sharing occurs in PageRank [6].
# §3.2.2.1(ii): The algorithm iteratively updates a rank for each document by adding up contributions from documents that link to it.
# §3.2.2.1(iii): On each iteration, each document sends a contribution of r / by n to its neighbors, where r is its rank and n is its number of neighbors.
# §3.2.2.1(iv): It then updates its rank to alpha / N + (1 - alpha) * sum(c[i]), where the sum is over the contributions it received and N is the total number of documents.
# §3.2.2.1(v): We can write PageRank in Spark as follows ...
"""\
    // Load graph as an RDD of (URL, outlinks) pairs
    val links = spark.textFile(...).map(...).persist();
    var ranks = ???; // RDD of (URL, rank) pairs
    for (i <- 1 to ITERATIONS) {
        // Build an RDD of (targetURL, float) pairs
        // with the contributions sent by each page
        val contribs = links.join(ranks).flatMap(
            (url, (links, rank)) => links.map(dest => (dest, rank / links.size))
        );
        // Sum contributions by URL and get new ranks
        ranks = contribs.reduceByKey((x, y) => x + y).mapValues(sum => a/N + (1 - a) * sum);
    }
"""
#---------------------------------------------------------------------------------------------------
# §3.2.2.2(i): This program leads to the RDD lineage graph in Figure 3.
# §3.2.2.2(ii): On each iteration, we create a new ranks dataset based on the contribs and ranks from the previous iteration and the static links dataset.
# §3.2.2.2(iii): One interesting feature of this graph is that it grows longer with the number of iterations.
# §3.2.2.2(iv): Thus, in a job with many iterations, it may be necessary to reliably replicate some of the versions of ranks to reduce fault recovery times [20].
# §3.2.2.2(v): The user can call persist with a RELIABLE flag to do this.
# §3.2.2.2(vi): However, note that the links dataset does not need to be replicated, because partitions of it can be rebuilt efficiently by rerunning a map on blocks of the input file.
# §3.2.2.2(vii): This dataset will typically be much larger than ranks, because each document has many links but only one number as its rank, so recovering it using lineage saves time over systems that checkpoint a program’s entire in-memory state.
#---------------------------------------------------------------------------------------------------
# §3.2.2.3(i): Finally, we can optimize communication in PageRank by controlling the partitioning of the RDDs.
# §3.2.2.3(ii): If we specify a partitioning for links (e.g., hash-partition the link lists by URL across nodes), we can partition ranks in the same way and ensure that the join operation between links and ranks requires no communication (as each URL’s rank will be on the same machine as its link list).
# §3.2.2.3(iii): We can also write a custom Partitioner class to group pages that link to each other together (e.g., partition the URLs by domain name).
# §3.2.2.3(iv): Both optimizations can be expressed by calling partitionBy when we define links ...
"""\
    links = spark.textFile("...").map(...).partitionBy(myPartFunc).persist();
"""
#===================================================================================================
# §4: Representing RDDs
#---------------------------------------------------------------------------------------------------
# §4.1(i): One of the challenges in providing RDDs as an abstraction is choosing a representation for them that can track lineage across a wide range of transformations.
# §4.1(ii): Ideally, a system implementing RDDs should provide as rich a set of transformation operators as possible (e.g., the ones in Table 2), and let users compose them in arbitrary ways.
# §4.1(iii): We propose a simple graph-based representation for RDDs that facilitates these goals.
# §4.1(iv): We have used this representation in Spark to support a wide range of transformations without adding special logic to the scheduler for each one, which greatly simplified the system design.
#---------------------------------------------------------------------------------------------------
# §4.2(i): In a nutshell, we propose representing each RDD through a common interface that exposes five pieces of information: a set of partitions, which are atomic pieces of the dataset; a set of dependencies on parent RDDs;
# §4.2(ii): a function for computing the dataset based on its parents;
# §4.2(iii): and metadata about its partitioning scheme and data placement.
# §4.2(iv): For example, an RDD representing an HDFS file has a partition for each block of the file and knows which machines each block is on.
# §4.2(v): Meanwhile, the result of a map on this RDD has the same partitions, but appliesthe map function to the parent’s data when computing its elements.
# §4.2(vi): We summarize this interface in Table 3.
#---------------------------------------------------------------------------------------------------
# Table 3: Interface used to represent RDDs in Spark
# Table 3(i):   Operation:                Meaning
# Table 3(ii):  partitions():             Return a list of Partition objects
# Table 3(iii): preferredLocations(p):    List nodes where partition p can be accessed faster due to data locality
# Table 3(iv):  dependencies():           Return a list of dependencies
# Table 3(v):   iterator(p, parentIters): Compute the elements of partition p given iterators for its parent partitions
# Table 3(vi):  partitioner():            Return metadata specifying whether the RDD is hash/range partitioned
#---------------------------------------------------------------------------------------------------
# §4.3(i): The most interesting question in designing this interface is how to represent dependencies between RDDs.
# §4.3(ii): We found it both sufficient and useful to classify dependencies into two types: narrow dependencies, where each partition of the parent RDD is used by at most one partition of the child RDD, wide dependencies, where multiple child partitions may depend on it.
# §4.3(iii): For example, map leads to a narrow dependency, while join leads to to wide dependencies (unless the parents are hash-partitioned).
# §4.3(iv): Figure 4 shows other examples.
#---------------------------------------------------------------------------------------------------
# §4.4(i): This distinction is useful for two reasons. First, narrow dependencies allow for pipelined execution on one cluster node, which can compute all the parent partitions.
# §4.4(ii): For example, one can apply a map followed by a filter on an element-by-element basis.
# §4.4(iii): In contrast, wide dependencies require data from all parent partitions to be available and to be shuffled across the nodes using a MapReduce-like operation.
# §4.4(iv): Second, recovery after a node failure is more efficient with a narrow dependency, as only the lost parent partitions need to be recomputed, and they can be recomputed in parallel on different nodes.
# §4.4(v): In contrast, in a lineage graph with wide dependencies, a single failed node might cause the loss of some partition from all the ancestors of an RDD, requiring a complete re-execution.
#===================================================================================================
# §4.5(i): This common interface for RDDs made it possible to implement most transformations in Spark in less than 20 lines of code.
# §4.5(ii): Indeed, even new Spark users have implemented new transformations (e.g., sampling and various types of joins) without knowing the details of the scheduler.
# §4.5(iii): We sketch some RDD implementations below.
#---------------------------------------------------------------------------------------------------
# §4.5.1(i): HDFS files: The input RDDs in our samples have been files in HDFS.
# §4.5.1(ii): For these RDDs, partitions returns one partition for each block of the file (with the block’s offset stored in each Partition object), preferredLocations gives the nodes the block is on, and iterator reads the block.
#---------------------------------------------------------------------------------------------------
# §4.5.2(i): map: Calling map on any RDD returns a MappedRDD object.
# §4.5.2(ii): This object has the same partitions and preferred locations as its parent, but applies the function passed to map to the parent’s records in its iterator method.
#---------------------------------------------------------------------------------------------------
# §4.5.3(i): union: Calling union on two RDDs returns an RDD whose partitions are the union of those of the parents.
# §4.5.3(ii): Each child partition is computed through a narrow dependency on the corresponding parent.
#---------------------------------------------------------------------------------------------------
# §4.5.4: sample: Sampling is similar to mapping, except that the RDD stores a random number generator seed for each partition to deterministically sample parent records.
#---------------------------------------------------------------------------------------------------
# §4.5.5(i): join: Joining two RDDs may lead to either two narrow dependencies (if they are both hash/range partitioned with the same partitioner), two wide dependencies, or a mix (if one parent has a partitioner and one does not).
# §4.5.5(ii): In either case, the output RDD has a partitioner (either one inherited from the parents or a default hash partitioner).
#===================================================================================================
# §5: Implementation
#---------------------------------------------------------------------------------------------------
# §5.0.1(i): We have implemented Spark in about 14,000 lines of Scala.
# §5.0.1(ii): The system runs over the Mesos cluster manager [17], allowing it to share resources with Hadoop, MPI and other applications.
# §5.0.1(iii): Each Spark program runs as a separate Mesos application, with its own driver (master) and workers, and resource sharing between these applications is handled by Mesos.
#---------------------------------------------------------------------------------------------------
# §5.0.2: Spark can read data from any Hadoop input source (e.g., HDFS or HBase) using Hadoop’s existing input plugin APIs, and runs on an unmodified version of Scala.
#---------------------------------------------------------------------------------------------------
# §5.0.3:  We now sketch several of the technically interesting parts of the system: our job scheduler (§5.1), our Spark interpreter allowing interactive use (§5.2), memory management (§5.3), and support for checkpointing (§5.4).
#===================================================================================================
# §5.1: Job Scheduling
#---------------------------------------------------------------------------------------------------
# §5.1.1: Spark’s scheduler uses our representation of RDDs, described in Section 4.
#---------------------------------------------------------------------------------------------------
# §5.1.2(i): Overall, our scheduler is similar to Dryad’s [19], but it additionally takes into account which partitions of persistent RDDs are available in memory.
# §5.1.2(ii): Whenever a user runs an action (e.g., count or save) on an RDD, the scheduler examines that RDD’s lineage graph to build a DAG of stages to execute, as illustrated in Figure 5.
# §5.1.2(iii): Each stage contains as many pipelined transformations with narrow dependencies as possible.
# §5.1.2(iv): The boundaries of the stages are the shuffle operations required for wide dependencies, or any already computed partitions that can short-circuit the computation of a parent RDD.
# §5.1.2(v): The scheduler then launches tasks to compute missing partitions from each stage until it has computed the target RDD.
#---------------------------------------------------------------------------------------------------
# §5.1.2(i): Our scheduler assigns tasks to machines based on data locality using delay scheduling [32].
# §5.1.2(ii): If a task needs to process a partition that is available in memory on a node, we send it to that node.
# §5.1.2(iii): Otherwise, if a task processes a partition for which the containing RDD provides preferred locations (e.g., an HDFS file), we send it to those.
#---------------------------------------------------------------------------------------------------
# §5.1.3: For wide dependencies (i.e., shuffle dependencies), we currently materialize intermediate records on the nodes holding parent partitions to simplify fault recovery, much like MapReduce materializes map outputs.
#---------------------------------------------------------------------------------------------------
# §5.1.4(i): If a task fails, we re-run it on another node as long as its stage’s parents are still available.
# §5.1.4(ii): If some stages have become unavailable (e.g., because an output from the “map side” of a shuffle was lost), we resubmit tasks to compute the missing partitions in parallel.
# §5.1.4(iii): We do not yet tolerate scheduler failures, though replicating the RDD lineage graph would be straightforward.
#---------------------------------------------------------------------------------------------------
# §5.1.5(i): Finally, although all computations in Spark currently run in response to actions called in the driver program, we are also experimenting with letting tasks on the cluster (e.g., maps) call the lookup operation, which provides random access to elements of hash-partitioned RDDs by key.
# §5.1.5(ii): In this case, tasks would need to tell the scheduler to compute the required partition if it is missing.
#===================================================================================================
# §5.2: Interpreter Integration
#---------------------------------------------------------------------------------------------------
# §5.2.1(i): Scala includes an interactive shell similar to those of Ruby and Python.
# §5.2.1(ii): Given the low latencies attained with in-memory data, we wanted to let users run Spark interactively from the interpreter to query big datasets.
#---------------------------------------------------------------------------------------------------
# §5.2.2(i): The Scala interpreter normally operates by compiling a class for each line typed by the user, loading it into the JVM, and invoking a function on it.
# §5.2.2(ii): This class includes a singleton object that contains the variables or functions on that line and runs the line’s code in an initialize method.
# §5.2.2(iii): For example, if the user types var x = 5 followed by println(x), the interpreter defines a class called Line1 containing x and causes the second line to compile to println(Line1.getInstance().x).
#---------------------------------------------------------------------------------------------------
# §5.2.3: We made two changes to the interpreter in Spark:
#---------------------------------------------------------------------------------------------------
# §5.2.3.1: Class shipping: To let the worker nodes fetch the bytecode for the classes created on each line, we made the interpreter serve these classes over HTTP.
#---------------------------------------------------------------------------------------------------
# §5.2.3.2(i): Modified code generation: Normally, the singleton object created for each line of code is accessed through a static method on its corresponding class.
# §5.2.3.2(ii): This means that when we serialize a closure referencing a variable defined on a previous line, such as Line1.x in the example above, Java will not trace through the object graph to ship the Line1 instance wrapping around x.
# §5.2.3.2(iii): Therefore, the worker nodes will not receive x.
# §5.2.3.2(iv): We modified the code generation logic to reference the instance of each line object directly.
#---------------------------------------------------------------------------------------------------
# §5.2.4: Figure 6 shows how the interpreter translates a set of lines typed by the user to Java objects after our changes.
#---------------------------------------------------------------------------------------------------
# §5.2.5(i): We found the Spark interpreter to be useful in processing large traces obtained as part of our research and exploring datasets stored in HDFS.
# §5.2.5(i): We also plan to use torun higher-level query languages interactively, e.g., SQL.
#===================================================================================================
# §5.3: Memory Management
#---------------------------------------------------------------------------------------------------
# §5.3.1(i): Spark provides three options for storage of persistent RDDs: in-memory storage as deserialized Java objects, in-memory storage as serialized data, and on-disk storage.
# §5.3.1(ii): The first option provides the fastest performance, because the Java VM can access each RDD element natively.
# §5.3.1(iii): The second option lets users choose a more memory-efficient representation than Java object graphs when space is limited, at the cost of lower performance.
# §5.3.1(iv): The third option is useful for RDDs that are too large to keep in RAM but costly to recompute on each use.
#---------------------------------------------------------------------------------------------------
# §5.3.2(i): To manage the limited memory available, we use an LRU eviction policy at the level of RDDs.
# §5.3.2(ii): When a new RDD partition is computed but there is not enough space to store it, we evict a partition from the least recently accessed RDD, unless this is the same RDD as the one with the new partition.
# §5.3.2(iii): In that case, we keep the old partition in memory to prevent cycling partitions from the same RDD in and out.
# §5.3.2(iv): This is important because most operations will run tasks over an entire RDD, so it is quite likely that the partition already in memory will be needed in the future.
# §5.3.2(v): We found this default policy to work well in all our applications so far, but we also give users further control via a “persistence priority” for each RDD.
#---------------------------------------------------------------------------------------------------
# §5.3.3(i): Finally, each instance of Spark on a cluster currently has its own separate memory space.
# §5.3.3(ii): In future work, we plan to investigate sharing RDDs across instances of Spark through a unified memory manager.
#===================================================================================================
# §5.4: Support for Checkpointing
#---------------------------------------------------------------------------------------------------
# §5.4.1(i): Although lineage can always be used to recover RDDs after a failure, such recovery may be time-consuming for RDDs with long lineage chains.
# §5.4.1(ii): Thus, it can be helpful to checkpoint some RDDs to stable storage.
#---------------------------------------------------------------------------------------------------
# §5.4.2(i): In general, checkpointing is useful for RDDs with long lineage graphs containing wide dependencies, such as the rank datasets in our PageRank example (§3.2.2).
# §5.4.2(ii): In these cases, a node failure in the cluster may result in the loss of some slice of data from each parent RDD, requiring a full recomputation [20].
# §5.4.2(iii): In contrast, for RDDs with narrow dependencies on data in stable storage, such as the points in our logistic regression example (§3.2.1) and the link lists in PageRank, checkpointing may never be worthwhile.
# §5.4.2(iv): If a node fails, lost partitions from these RDDs can be recomputed in parallel on other nodes, at a fraction of the cost of replicating the whole RDD.
#---------------------------------------------------------------------------------------------------
# §5.4.3(i): Spark currently provides an API for checkpointing (a REPLICATE flag to persist), but leaves the decision of which data to checkpoint to the user.
# §5.4.3(ii): However, we are also investigating how to perform automatic checkpointing.
# §5.4.3(iii): Because our scheduler knows the size of each dataset as well as the time it took to first compute it, it should be able to select an optimal set of RDDs to checkpoint to minimize system recovery time [30].
#---------------------------------------------------------------------------------------------------
# §5.4.4(i): Finally, note that the read-only nature of RDDs makes them simpler to checkpoint than general shared memory.
# §5.4.4(ii): Because consistency is not a concern, RDDs can be written out in the background without requiring program pauses or distributed snapshot schemes.
#===================================================================================================
