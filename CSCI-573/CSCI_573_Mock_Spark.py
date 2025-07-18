#===============================================================================
# Mock Spark, by Lon Cherryholmes, Sr.
# CSCI-573: Big Data Computing and Analytics
# Professor: Manar Alsaid, East Texas A&M University
#===============================================================================
# Resilient Distributed Datasets:
#    A Fault-Tolerant Abstraction for In-Memory Cluster Computing
# by Matei Zaharia, Mosharaf Chowdhury, Tathagata Das, Ankur Dave, Justin Ma,
#    Murphy McCauley, Michael J. Franklin, Scott Shenker, and Ion Stoica
# at University of California, Berkeley
#-------------------------------------------------------------------------------
# Abstract:
# Abstract(i): We present Resilient Distributed Datasets (RDDs), ...
machines = ["Brazos", "Colorado", "Guadalupe", "Pecos"] # ... a distributed ...
N_MACHINES = len(machines) # ... memory abstraction that lets programmers ...
class Machine: # ... perform in-memory computations on large clusters ...
    def __init__(self, id): # ... in a fault-tolerant manner.
        self.id = id
        self.name = machines[id]
        self.files = defaultdict(list)
        self.records = defaultdict(list)
    def __repr__(self):
        return f"{self.id} {self.name} {pformat(self.records)}"
#-------------------------------------------------------------------------------
# Abstract(ii): RDDs are motivated by two types of applications that ...
# Abstract(ii): ... current computing frameworks handle inefficiently: ...
# Abstract(ii): ... iterative algorithms and interactive data mining tools.
# Abstract(iii): In both cases, keeping data in memory ...
# Abstract(iii): ... can improve performance by an order of magnitude.
#-------------------------------------------------------------------------------
# §1: Introduction
#export PYTHONHASHSEED=42
#export SPARK_LOCAL_IP=172.28.64.15
import pickle
from pprint import pformat, pprint
from functools import reduce
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
#===============================================================================
# §2: Resilient Distributed Datasets (RDDs)
# §2(i): This section provides an overview of RDDs.
# §2(ii): We first define RDDs (§2.1) ...
# §2(ii): ... and introduce their programming interface in Spark (§2.2).
# §2(iii): We then compare RDDs ...
# §2(iii): ... with finer-grained shared memory abstractions (§2.3).
# §2(iv): Finally, we discuss limitations of the RDD model (§2.4).
#-------------------------------------------------------------------------------
# §2.1: RDD Abstraction
class MockRDD: # §2.1(i): Formally, an RDD is a read-only, partitioned ...
               # §2.1(i): ... collection of records.
#   ----------------------------------------------------------------------------
    def __init__(self,
        op=None, deps=None, args=None,
        records=None, num_parts=None,
        partitioner=None):
        self.op = op
        self.uid = None
        self.deps = deps
        self.args = args
        if records: self.records = records
        self.num_parts = num_parts
        self.partitioner = partitioner
#-------------------------------------------------------------------------------
# §2.1(ii): RDDs can only be created through deterministic ...
# §2.1(ii): ...  operations on either (1) data in stable storage ...
# §2.1(ii): ... or (2) other RDDs.
#-------------------------------------------------------------------------------
class SpockContext:
    def textFile(self, filename, minPartitions=1):
        num_parts = self.defaultParallelism \
                 if self.defaultParallelism > minPartitions \
               else minPartitions
        with open(filename) as file:
            records = [line.rstrip('\n') for line in file]
            return MockRDD(records=records, num_parts=num_parts)
    defaultParallelism = 2
    def parallelize(self, sequence, numSlices=None):
        num_parts = numSlices if numSlices else self.defaultParallelism
        return MockRDD(records=list(sequence), num_parts=num_parts)
#-------------------------------------------------------------------------------
from pyspark import SparkContext
from pyspark.rdd import portable_hash
spark = SparkContext.getOrCreate()
spark.setLogLevel("ERROR")
spock = SpockContext()
#-------------------------------------------------------------------------------
# §2.1(iii): We call these operations transformations ...
# §2.1(iii): ... to differentiate them from other operations on RDDs.
# §2.1(iv): Examples of transformations include map, filter, and join.
def _map(records, func):    return [func(x) for x in records]
def _filter(records, func): return [x for x in records if func(x)]
def _join(records, other_records, numPartitions):
    memory = dict()
    for x in records:
        memory.setdefault(x[0], []).append(x)
    new_records = []
    for y in other_records:
        if y[0] in memory:
            for x in memory[y[0]]:
                assert x[0] == y[0]
                new_records.append((x[0], (x[1], y[1])))
    return new_records
#-------------------------------------------------------------------------------
# §2.1(v): RDDs do not need to be materialized at all times.
# §2.1(vi): Instead, an RDD has enough information about how it was derived ...
# §2.1(vi): ... from other datasets (its lineage) to compute its partitions ...
# §2.1(vi): ... from data in stable storage.
#-------------------------------------------------------------------------------
def HashPartitioner(key): return hash(key)
def _compute(self, partitioner=None):
    if self.uid is None:
        self.uid = f"{self.op if self.op else ''}{next_id()}"
        if self.op: # Mock scheduling partition tasks
            if self.op in ["cogroup", "groupByKey", "join", "reduceByKey"]:
                if partitioner is None:
                    partitioner = HashPartitioner
            args = ( [dep.compute(partitioner) for dep in self.deps]
                   + list(self.args)
                   )
            if False:
                for n in range(self.num_parts):
                    cluster[n].records[self.uid] = \
                        cluster[n].executor(self.op, args)
            if True:
                with ThreadPoolExecutor(max_workers=self.num_parts) \
                  as executor:
                    futures = {
                        executor.submit(
                            Machine.executor,
                            cluster[MACHINE],
                            self.op,
                            args): MACHINE
                        for MACHINE in range(self.num_parts)
                    }
                    for future in as_completed(futures):
                        n = futures[future]
                        cluster[n].records[self.uid] = future.result()
        else: # Mock copying partitions to machines in the cluster
            if partitioner:
                for record in self.records:
                    n = partitioner(record[0]) % self.num_parts
                    cluster[n].records[self.uid].append(record)
            else:
                part_size = math.ceil(len(self.records) / self.num_parts)
                for n in range(self.num_parts):
                    cluster[n].records[self.uid] = \
                        self.records[n * part_size:(n + 1) * part_size]
    return self.uid
setattr(MockRDD, "compute", _compute); del _compute
#-------------------------------------------------------------------------------
# §2.1(vii): This is a powerful property: in essence, a program cannot ...
# §2.1(vii): ... reference an RDD that it cannot reconstruct after a failure.
unique_id = 0
def next_id(): global unique_id; unique_id += 1; return unique_id
#-------------------------------------------------------------------------------
# §2.1(viii): Finally, users can control two other aspects of RDDs: ...
# §2.1(viii): ... persistence and partitioning.
def _persist(self, storage='memory'): # §2.1(ix): Users can indicate which ...
    self.persisted = True # ... RDDs they will reuse and choose a storage ...
    self.storage = storage # ... strategy for them (e.g., in-memory storage).
# §2.1(x): They can also ask that an RDD’s elements be partitioned across ...
# §2.1(x): ... machines based on a key in each record.
# §2.1(xi): This is useful for placement optimizations, such as ...
# §2.1(xi): ... ensuring that two datasets that will be joined together ...
# §2.1(xi): ... are hash-partitioned in the same way.
#===============================================================================
# §2.2: Spark Programming Interface
#-------------------------------------------------------------------------------
# §2.2.0.1(i): Spark exposes RDDs through a language-integrated API similar ...
# §2.2.0.1(i): ... to DryadLINQ [31] and FlumeJava [8], where each dataset ...
MockRDD_ops = dict() # §2.2.0.1(i): ... is represented as an object and ...
def _executor(self, op, args): # §2.2.0.1(i): ... transformations are ...
    match op: # §2.2.0.1(i): ... invoked using methods on these objects.
        case "map":         args = (self.records[args[0]], args[1])
        case "filter":      args = (self.records[args[0]], args[1])
        case "flatMap":     args = (self.records[args[0]], args[1])
        case "sample":      args = (self.records[args[0]], *args[1:])
        case "groupByKey":  args = (self.records[args[0]], *args[1:])
        case "reduceByKey": args = (self.records[args[0]], *args[1:])
        case "union":       args = (self.records[args[0]],
                                    self.records[args[1]])
        case "join":        args = (self.records[args[0]],
                                    self.records[args[1]],
                                    args[2])
        case "cogroup":     args = (self.records[args[0]],
                                    self.records[args[1]])
        case "cartesian":   args = (self.records[args[0]],
                                    self.records[args[1]])
        case "mapValues":   args = (self.records[args[0]], args[1])
        case "sortBy":      args = (self.records[args[0]], *args[1:])
        case "partitionBy": args = (self.records[args[0]], *args[1:])
        case "persist":     args = (self.records[args[0]], *args[1:])
        case _: raise Exception("[executor] Unknown operation {op}.")
    return MockRDD_ops[op](*args)
setattr(Machine, "executor", _executor); del _executor
#-------------------------------------------------------------------------------
# §2.2.0.2(i): Programmers start by defining one or more RDDs ...
def test_2_2_0_2(context): # §2.2.0.2(i): ... through transformations on ...
    # §2.2.0.2(i): ... data in stable storage (e.g., map and filter).
    records = [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')]
    rdd_1 = context.parallelize(records)
    rdd_2 = rdd_1.map(lambda x: (x[0], x[1].upper()))
    rdd_3 = rdd_2.filter(lambda x: x[0] % 2 == 0)
    rdd_4 = rdd_1.join(rdd_3)
    # §2.2.0.2(ii): They can then use these RDDs in actions, which are ...
    # §2.2.0.2(ii): ... operations that return a value to the application or ...
    # §2.2.0.2(ii): ... export data to a storage system.
    # §2.2.0.2(iii): Examples of actions include ...
    pprint(rdd_4.count()) # §2.2.0.2(iii): ... count (which returns the ...
                    # §2.2.0.2(iii): ... number of elements in the dataset), ...
    pprint(rdd_4.collect()) # §2.2.0.2(iii): ... collect (which returns the ...
                            # §2.2.0.2(iii): ... elements themselves), and ...
#   rdd_4.save("rdd_4.pkl") # §2.2.0.2(iii): ... save (which outputs the ...
                            # §2.2.0.2(iii): ... dataset to a storage system).
#-------------------------------------------------------------------------------
# §2.2.0.2(iv): Like DryadLINQ, Spark computes RDDs lazily the first time ...
# §2.2.0.2(iv): ... they are used in an action, so that it can pipeline ...
# §2.2.0.2(iv): ... transformations.
#-------------------------------------------------------------------------------
# §2.2.0.3(i): In addition, programmers can call a persist method to ...
# §2.2.0.3(i): ... indicate which RDDs they want to reuse in future operations.
# §2.2.0.3(ii): Spark keeps persistent RDDs in memory by default, but it can ...
# §2.2.0.3(ii): ... spill them to disk if there is not enough RAM.
# §2.2.0.3(iii): Users can also request other persistence strategies, ...
# §2.2.0.3(iii): ... such as storing the RDD only on disk or ...
# §2.2.0.3(iii): ... replicating it across machines, through flags to persist.
# §2.2.0.3(iv): Finally, users can set a persistence priority on each RDD ...
# §2.2.0.3(iv): ... to specify which in-memory data should spill to disk first.
#===============================================================================
# §2.2.1: Example: Console Log Mining
#-------------------------------------------------------------------------------
# §2.2.1.1(i): Suppose that a web service is experiencing errors and an ...
# §2.2.1.1(i): ... operator wants to search terabytes of logs ...
# §2.2.1.1(i): ... in the Hadoop filesystem (HDFS) to find the cause.
hdfs_log = [
    "INFO\t2025-06-26\t23:53\tStartup complete.",
    "ERROR\t2025-06-26\t23:54\tMySQL connection failed.",
    "WARN\t2025-06-26\t23:55\tDisk space low.",
    "ERROR\t2025-06-26\t23:56\tHDFS block missing.",
    "ERROR\t2025-06-26\t23:57\tMySQL timeout.",
    "INFO\t2025-06-26\t23:58\tShutdown complete.",
    "ERROR\t2025-06-26\t23:59\tHDFS nodename lost."
]
# §2.2.1.1(ii): Using Spark, the operator can load just the error messages ...
# §2.2.1.1(ii): ... from the logs into RAM across a set of nodes and ...
# §2.2.1.1(ii): ... query them interactively.
errors = None # §2.2.1.1(iii): She would first type the following Scala code:
def example_2_2_1_1(context):
    global errors
    # §2.2.1.1(iv): Line 1 defines an RDD backed by an ...
    # §2.2.1.1(iv): ... HDFS file (as a collection of lines of text), ...
    lines = context.parallelize(hdfs_log) #.textFile("hdfs://...")
    # §2.2.1.1(iv): ... while line 2 derives a filtered RDD from it.
    errors = lines.filter(lambda line: line.startswith("ERROR"))
    errors.persist() # §2.2.1.1(v): Line 3 then asks for errors to persist ...
    # §2.2.1.1(v): ... in memory so that it can be shared across queries.
    # §2.2.1.1(vi): Note that the argument to filter is Scala syntax ...
    # §2.2.1.1(vi): ... for a closure.
#-------------------------------------------------------------------------------
# §2.2.1.2(i): At this point, no work has been performed on the cluster.
# §2.2.1.2(ii): However, the user can now use the RDD in actions, ...
# §2.2.1.2(ii): ... e.g., to count the number of messages:
def example_2_2_1_2(context):
    pprint(["errors count", errors.count()])
#-------------------------------------------------------------------------------
# §2.2.1.3(i): The user can also perform further transformations on the RDD ...
# §2.2.1.3(i): ... and use their results, as in the following lines:
def example_2_2_1_3(context):
    # Count errors mentioning MySQL:
    count = errors.filter(lambda line: line.find("MySQL") >= 0).count()
    pprint(["MySQL count", count])
    # Return the time fields of errors mentioning HDFS as an array
    # (assuming time is field number 3 in a tab-separated format):
    times = errors.filter(lambda line: line.find("HDFS") >= 0) \
                  .map(lambda line: line.split("\t")[2]) \
                  .collect()
    pprint(["HDFS times", times])
#-------------------------------------------------------------------------------
# §2.2.1.4(i): After the first action involving errors runs, Spark will ...
# §2.2.1.4(i): ... store the partitions of errors in memory, ...
# §2.2.1.4(i): ... greatly speeding up subsequent computations on it.
# §2.2.1.4(ii): Note that the base RDD, lines, is not loaded into RAM.
# §2.2.1.4(iii): This is desirable because the error messages might only ...
# §2.2.1.4(iii): ... be a small fraction of the data ...
# §2.2.1.4(iii): ... (small enough to fit into memory).
#===============================================================================
# §3: Spark Programming Interface
#-------------------------------------------------------------------------------
# §3.0.1(i): Spark provides the RDD abstraction through a language- ...
# §3.0.1(i): ... integrated API similar to DryadLINQ [31] in Scala [2], a ...
# §3.0.1(i): ... statically typed functional programming language ...
# §3.0.1(i): ... for the Java VM.
# §3.0.1(ii): We chose Scala due to its combination of ...
# §3.0.1(ii): ... conciseness (which is convenient for interactive use) ...
# §3.0.1(ii): ... and efficiency (due to static typing).
# §3.0.1(iii): However, nothing about the RDD abstraction ...
# §3.0.1(iii): ... requires a functional language.
#-------------------------------------------------------------------------------
# §3.0.2(i): To use Spark, developers write a driver program ...
# §3.0.2(i): ... that connects to a cluster of workers, as shown in Figure 2.
# §3.0.2(ii): The driver defines one or more RDDs and invokes actions on them.
# §3.0.2(iii): Spark code on the driver also tracks the RDDs lineage.
# §3.0.2(iv): The workers are long-lived processes ...
# §3.0.2(iv): ... that can store RDD partitions in RAM across operations.
#-------------------------------------------------------------------------------
# §3.0.3(i): As we showed in the log mining example in Section 2.2.1, ...
# §3.0.3(i): ... users provide arguments to RDD operations like map ...
# §3.0.3(i): ... by passing closures (function literals).
# §3.0.3(ii): Scala represents each closure as a Java object, and these ...
# §3.0.3(ii): ... objects can be serialized and loaded on another node ...
# §3.0.3(ii): ... to pass the closure across the network.
# §3.0.3(iii): Scala also saves any variables bound in the closure ...
# §3.0.3(iii): ... as fields in the Java object.
x = 5 # §3.0.3(iv): For example, one can write code like ...
def example_3_0(context): # §3.0.3(iv): ... to add 5 to each element of an RDD.
    rdd.map(lambda i: i + x)
#-------------------------------------------------------------------------------
# §3.0.4(i): RDDs themselves are statically typed ...
# §3.0.4(i): ... objects parametrized by an element type.
# §3.0.4(ii): For example, RDD[Int] is an RDD of integers.
# §3.0.4(iii): However, most of our examples ...
# §3.0.4(iii): ... omit types since Scala supports type inference.
#-------------------------------------------------------------------------------
# §3.0.5(i): Although our method of exposing RDDs in Scala is ...
# §3.0.5(i): ... conceptually simple, we had to work around issues with ...
# §3.0.5(i): ... Scala’s closure objects using reflection [33].
# §3.0.5(ii): We also needed more work to make Spark usable from the Scala ...
# §3.0.5(ii): ... interpreter, as we shall discuss in Section 5.2.
# §3.0.5(iii): Nonetheless, we did not have to modify the Scala compiler.
#===============================================================================
# §3.1 RDD Operations in Spark
#-------------------------------------------------------------------------------
# §3.1.1(i): Table 2 lists the main RDD ...
# §3.1.1(i): ... transformations and actions available in Spark.
# §3.1.1(ii): We give the signature of each operation, ...
# §3.1.1(ii): ... showing type parameters in square brackets.
# §3.1.1(iii): Recall that transformations are lazy operations that define ...
# §3.1.1(iii): ... a new RDD, while actions launch a computation to return ...
# §3.1.1(iii): ... a value to the program or write data to external storage.
#-------------------------------------------------------------------------------
# Table 2(i): Transformations and actions available on RDDs in Spark.
# Table 2(ii): Seq[T] denotes a sequence of elements of type T.
#===============================================================================
# Table 2.1: Transformations: ==================================================
#===============================================================================
# Table 2.1(i):     map(f: T => U): RDD[T] => RDD[U]
MockRDD_ops       ["map"] = _map; del _map
setattr(MockRDD,   "map", lambda self, func:
        MockRDD(op="map", deps=[self], args=(func,), num_parts=self.num_parts))
#-------------------------------------------------------------------------------
# Table 2.1(ii):    filter(f: T => Bool): RDD[T] => RDD[T]
MockRDD_ops       ["filter"] = _filter; del _filter
setattr(MockRDD,   "filter", lambda self, func:
        MockRDD(op="filter",
            deps=[self],
            args=(func,),
            num_parts=self.num_parts))
#-------------------------------------------------------------------------------
# Table 2.1(iii): flatMap(f: T => Seq[U]): RDD[T] => RDD[U]
def _flatMap(records, func):
    return [y for x in records for y in func(x)]
MockRDD_ops       ["flatMap"] = _flatMap; del _flatMap
setattr(MockRDD,   "flatMap", lambda self, func:
        MockRDD(op="flatMap",
            deps=[self],
            args=(func,),
            num_parts=self.num_parts))
#-------------------------------------------------------------------------------
# Table 2.1(iv): sample(fraction: Float): RDD[T] => RDD[T]
def _sample(records, withReplacement, fraction, seed):
    random.seed(seed) # Table 2.1(iv): (Deterministic sampling)
    return [x for x in records if random.random() < fraction]
MockRDD_ops       ["sample"] = _sample; del _sample
setattr(MockRDD,   "sample", lambda self, withReplacement, fraction, seed=42:
        MockRDD(op="sample",
            deps=[self],
            args=(withReplacement, fraction, seed),
            num_parts=self.num_parts))
#-------------------------------------------------------------------------------
# Table 2.1(v): groupByKey(): RDD[(K, V)] => RDD[(K, Seq[V])]
def _groupByKey(records, numPartitions): # Only for RDDs of key-value pairs
    grouped = dict()
    for k, v in records:
        grouped.setdefault(k, []).append(v)
    return list(grouped.items())
MockRDD_ops       ["groupByKey"] = _groupByKey; del _groupByKey
setattr(MockRDD,   "groupByKey", lambda self, numPartitions=None:
        MockRDD(op="groupByKey",
            deps=[self],
            args=(numPartitions,),
            num_parts=self.num_parts))
#-------------------------------------------------------------------------------
# Table 2.1(vi): reduceByKey(f: (V, V) => V): RDD[(K, V)] => RDD[(K, V)]
def _reduceByKey(records, func, numPartitions):
    reduced = dict() # Only for RDDs of key-value pairs
    for k, v in records:
        reduced.setdefault(k, []).append(v)
    return [(k, reduce(func, vlist)) for k, vlist in reduced.items()]
MockRDD_ops       ["reduceByKey"] = _reduceByKey; del _reduceByKey
setattr(MockRDD,   "reduceByKey", lambda self, func, numPartitions=None:
        MockRDD(op="reduceByKey",
            deps=[self],
            args=(func, numPartitions),
            num_parts=self.num_parts))
#-------------------------------------------------------------------------------
# Table 2.1(vii): union(): (RDD[T], RDD[T]) => RDD[T]
def _union(records, other_records): return records + other_records
MockRDD_ops       ["union"] = _union; del _union
setattr(MockRDD,   "union", lambda self, other:
        MockRDD(op="union",
            deps=[self, other],
            args=(),
            num_parts=self.num_parts))
#-------------------------------------------------------------------------------
# Table 2.1(viii):  join(): (RDD[(K, V)], RDD[(K, W)]) => RDD[(K, (V, W))]
MockRDD_ops       ["join"] = _join; del _join
setattr(MockRDD,   "join", lambda self, other, numPartitions=None:
        MockRDD(op="join",
            deps=[self, other],
            args=(numPartitions,),
            num_parts=self.num_parts))
#-------------------------------------------------------------------------------
# Table 2.1(ix): cogroup(): (RDD[(K, V)], RDD[(K, W)])
# Table 2.1(ix):          => RDD[(K, (Seq[V], Seq[W]))]
def _cogroup(records, other_records):
    dict_self = defaultdict(list)
    for k, v in records:
        dict_self[k].append(v)
    dict_other = defaultdict(list)
    for k, w in other_records:
        dict_other[k].append(w)
    keys = set(dict_self.keys()) | set(dict_other.keys())
    result = []
    for k in keys:
        result.append((k, (dict_self[k], dict_other[k])))
    return result
MockRDD_ops       ["cogroup"] = _cogroup; del _cogroup
setattr(MockRDD,   "cogroup", lambda self, other:
        MockRDD(op="cogroup",
            deps=[self, other],
            args=(),
            num_parts=self.num_parts))
#-------------------------------------------------------------------------------
# Table 2.1(x): crossProduct(): (RDD[T], RDD[U]) => RDD[(T, U)]
def _cartesian(records, other_records):
    return [(x, y) for x in records for y in other_records]
MockRDD_ops       ["cartesian"] = _cartesian; del _cartesian
setattr(MockRDD,   "cartesian", lambda self, other:
        MockRDD(op="cartesian",
            deps=[self, other],
            args=(),
            num_parts=self.num_parts))
#-------------------------------------------------------------------------------
# Table 2.1(xi): mapValues(f: V => W): RDD[(K, V)] => RDD[(K, W)]
def _mapValues(records, func): # Table 2.1(xi): (Preserves partitioning)
    return [(k, func(v)) for k, v in records]
MockRDD_ops       ["mapValues"] = _mapValues; del _mapValues
setattr(MockRDD,   "mapValues", lambda self, func:
        MockRDD(op="mapValues",
            deps=[self],
            args=(func,),
            num_parts=self.num_parts))
#-------------------------------------------------------------------------------
# Table 2.1(xii): sort(c: Comparator[K]): RDD[(K, V)] => RDD[(K, V)]
def _sortBy(records, keyfunc, ascending, numPartitions):
    return sorted(records, key=keyfunc, reverse=not ascending)
MockRDD_ops["sortBy"] = _sortBy; del _sortBy
setattr(MockRDD, "sortBy",
    lambda self, keyfunc=None, ascending=True, numPartitions=None:
        MockRDD(op="sortBy",
            deps=[self],
            args=(keyfunc, ascending, numPartitions),
            num_parts=self.num_parts))
#-------------------------------------------------------------------------------
# Table 2.1(xiii): partitionBy(p: Partitioner[K]): RDD[(K, V)] => RDD[(K, V)]
def _partitionBy(records): return records
MockRDD_ops       ["partitionBy"] = _partitionBy; del _partitionBy
setattr(MockRDD,   "partitionBy",
    lambda self, numPartitions, partitionFunc=None:
        MockRDD(op="partitionBy",
            deps=[self],
            args=(),
            num_parts=numPartitions,
            partitioner=partitionFunc))
#===============================================================================
# Table 2.2: Actions: ==========================================================
#===============================================================================
# Table 2.2(i): count(): RDD[T] => Long
def _count(self):
    return len(self.collect())
setattr(MockRDD, "count", _count); del _count
#-------------------------------------------------------------------------------
# Table 2.2(ii): collect(): RDD[T] => Seq[T]
def _collect(self):
    uid = self.compute()
    return [x for n in range(self.num_parts) for x in cluster[n].records[uid]]
setattr(MockRDD, "collect", _collect); del _collect
#-------------------------------------------------------------------------------
# Table 2.2(iii): reduce(f: (T, T) => T): RDD[T] => T
def _reduce(self, func):
    iterator = iter(self.collect())
    result = next(iterator)
    for x in iterator:
        result = func(result, x)
    return result
setattr(MockRDD, "reduce", _reduce); del _reduce
#-------------------------------------------------------------------------------
# Table 2.2(iv): lookup(k: K): RDD[(K, V)] => Seq[V]
def _lookup(self, key): # Table 2.2(iv): (On hash/range partitioned RDDs)
    return [v for k, v in self.collect() if k == key]
setattr(MockRDD, "lookup", _lookup); del _lookup
#-------------------------------------------------------------------------------
# Table 2.2(v): save(path: String): (Outputs RDD to a storage system, HDFS)
def _save(self, path): # Table 2.2(iv): (On hash/range partitioned RDDs)
    with open(path, 'wb') as file:
        pickle.dump(self.collect(), path)
    return self
setattr(MockRDD, "save", _save); del _save
#-------------------------------------------------------------------------------
# §3.1.2(i): Note that some operations, such as join, ...
# §3.1.2(i): ... are only available on RDDs of key-value pairs.
# §3.1.2(ii): Also, our function names are chosen to match other APIs ...
# §3.1.2(ii): ... in Scala and other functional languages;
# §3.1.2(iii): for example, map is a one-to-one mapping, ...
# §3.1.2(iii): ... while flatMap maps each input value ...
# §3.1.2(iii): ... to one or more outputs (similar to the map in MapReduce).
#-------------------------------------------------------------------------------
# §3.1.3(i): In addition to these operators, users can ask for ...
# §3.1.3(i): ... an RDD to persist.
MockRDD_ops       ["persist"] = _persist; del _persist
setattr(MockRDD,   "persist", lambda self:
        MockRDD(op="persist", deps=[self], args=(), num_parts=self.num_parts))
#-------------------------------------------------------------------------------
# §3.1.3(ii): Furthermore, users can get an RDD’s partition order, which is ...
# §3.1.3(ii): ... represented by a Partitioner class, and partition another ...
setattr(MockRDD, "partitioner", None) # §3.1.3(ii): ... dataset according ...
def getNumPartitions(self): return self.num_parts # §3.1.3(ii): ... to it.
# §3.1.3(iii): Operations such as groupByKey, reduceByKey and sort ...
# §3.1.3(iii): ... automatically result in a hash or range partitioned RDD.
#===============================================================================
# §3.2: Example Applications
#-------------------------------------------------------------------------------
# §3.2.0(i): We complement the data mining example in Section 2.2.1 with ...
# §3.2.0(i): ... two iterative applications: logistic regression and PageRank.
# §3.2.0(ii): The latter also showcases how ...
# §3.2.0(ii): ... control of RDDs’ partitioning can improve performance.
#-------------------------------------------------------------------------------
# §3.2.1: Logistic Regression
#-------------------------------------------------------------------------------
# §3.2.1.1(i): Many machine learning algorithms are iterative in nature ...
# §3.2.1.1(i): ... because they run iterative optimization procedures, ...
# §3.2.1.1(i): ... such as gradient descent, to maximize a function.
# §3.2.1.1(ii): They can thus run much faster by keeping their data in memory.
#-------------------------------------------------------------------------------
import math     # §3.2.1.2(i): As an example, the following program ...
import random   # §3.2.1.2(i): ... implements logistic regression [14], a ...
points_data = [ # §3.2.1.2(i): ... common classification algorithm that ...
  "0.5,1.2,-1.3,1"  # §3.2.1.2(i): ... searches for a hyperplane w that ...
, "-0.3,0.8,0.5,-1" # §3.2.1.2(i): ... best separates two sets of points ...
, "1.0,-0.5,2.0,1"  # §3.2.1.2(i): ... (e.g., spam and non-spam emails).
, "-1.2,0.4,-0.7,-1" ]
#-------------------------------------------------------------------------------
class Point:
    def __init__(self, x, y):
        self.x = x # feature vector (list of floats)
        self.y = y # label (+1 or -1)
    def __repr__(self): return f"Point({self.x}, {self.y})"
#-------------------------------------------------------------------------------
def parsePoint(line):
    fields = line.strip().split(',')
    x = [float(v) for v in fields[:-1]]
    y = float(fields[-1])
    return Point(x, y)
#-------------------------------------------------------------------------------
# §3.2.1.2(ii): The algorithm uses gradient descent: it starts w at a random ...
# §3.2.1.2(ii): ... value, and on each iteration, it sums a function of w ...
# §3.2.1.2(ii): ... over the data to move w in a direction that improves it.
#-------------------------------------------------------------------------------
def example_3_2_1(context):
    DIMENSIONS = len(parsePoint(points_data[0]).x)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # §3.2.1.3(i): We start by defining a persistent RDD called points as ...
    # §3.2.1.3(i): ... the result of a map transformation on a text file ...
    # §3.2.1.3(i): ... that parses each line of text into a Point object.
    points = context.parallelize(points_data).map(parsePoint)
    points.persist()
    w = [random.uniform(-1, 1) for _ in range(DIMENSIONS)]
    def gradient_func(p):
        dot = sum(wj * xj for wj, xj in zip(w, p.x))
        coeff = (1 / (1 + math.exp(-p.y * dot)) - 1) * p.y
        return [xj * coeff for xj in p.x]
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # §3.2.1.3(ii): We then repeatedly run map and reduce on points to ...
    # §3.2.1.3(ii): ... compute the gradient at each step by ...
    # §3.2.1.3(ii): ... summing a function of the current w.
    ITERATIONS = 5
    for i in range(ITERATIONS):
        gradients = points.map(gradient_func).reduce(
            lambda a, b: [ai + bi for ai, bi in zip(a, b)]
        )
        w = [wj - gj for wj, gj in zip(w, gradients)]
        print("Weights (w):", w)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # §3.2.1.3(iii): Keeping points in memory across iterations can yield a ...
    # §3.2.1.3(iii): ... 20x speedup, as we show in Section 6.1.
#-------------------------------------------------------------------------------
# §3.2.2: PageRank
#-------------------------------------------------------------------------------
# §3.2.2.1(i): A more complex pattern of data sharing occurs in PageRank [6].
graph_data = [          # §3.2.2.1(ii): The algorithm iteratively updates a ...
    ("A", ["B", "C"]),  # §3.2.2.1(ii): ... rank for each document by adding ...
    ("B", ["C"]),       # §3.2.2.1(ii): ... up contributions from documents ...
    ("C", ["A"]),       # §3.2.2.1(ii): ... that link to it.
    ("D", ["C"])
]
#-------------------------------------------------------------------------------
def display_ranks(ranks):
    print("PageRank: ", end="")
    for url, rank in sorted(ranks.collect()):
        print(f" {url}: {rank:.4f}", end="")
    print()
#-------------------------------------------------------------------------------
# §3.2.2.1(iii): On each iteration, each document sends a contribution of ...
# §3.2.2.1(iii): ... "r / n" to its neighbors, where ...
# §3.2.2.1(iii): ... r is its rank and ...
# §3.2.2.1(iii): ... n is its number of neighbors.
# §3.2.2.1(iv): It then updates its rank to ...
# §3.2.2.1(iv): ... "alpha / N + (1 - alpha) * sum(c[i])", where the ...
# §3.2.2.1(iv): ... sum is over the contributions it received and ...
# §3.2.2.1(iv): ... N is the total number of documents.
# §3.2.2.1(v): We can write PageRank in Spark as follows ...
#-------------------------------------------------------------------------------
def example_3_2_2(context):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Load graph as an RDD of (URL, outlinks) pairs
    links = context.parallelize(graph_data, numSlices=1)
#   links = links.partitionBy(2, lambda key: portable_hash(key))
    links.persist()
    urls = [url for url, _ in graph_data]
    N = len(urls)
    alpha = 0.15
    ranks = context.parallelize([(url, 1.0) for url in urls], numSlices=1)
#   ranks = ranks.partitionBy(2, lambda key: portable_hash(key))
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # §3.2.2.2(i): This program leads to the RDD lineage graph in Figure 3.
    # §3.2.2.2(ii): On each iteration, we create a new ranks dataset based ...
    # §3.2.2.2(ii): ... on the contribs and ranks from the previous ...
    # §3.2.2.2(ii): ... iteration and the static links dataset.
    ITERATIONS = 5
    for i in range(ITERATIONS):
        # Build an RDD of (targetURL, float) pairs
        # with the contributions sent by each page
        joined = links.join(ranks)
        def compute_contribs(item):
            url, (outlinks, rank) = item
            n = len(outlinks)
            if n == 0:
                return []
            return [(dest, rank / n) for dest in outlinks]
        contribs = joined.flatMap(compute_contribs)
        contribs_summed = contribs.reduceByKey(lambda x, y: x + y)
        # Sum contributions by URL and get new ranks
        def update_rank(sum_contrib):
            return alpha / N + (1 - alpha) * sum_contrib
        ranks = contribs_summed.map(lambda kv: (kv[0], update_rank(kv[1])))
        display_ranks(ranks)
#-------------------------------------------------------------------------------
# §3.2.2.2(iii): One interesting feature of this graph is ...
# §3.2.2.2(iii): ... that it grows longer with the number of iterations.
# §3.2.2.2(iv): Thus, in a job with many iterations, it may be necessary ...
# §3.2.2.2(iv): ... to reliably replicate some of the versions of ranks ...
# §3.2.2.2(iv): ... to reduce fault recovery times [20].
# §3.2.2.2(v): The user can call persist with a RELIABLE flag to do this.
# §3.2.2.2(vi): However, note that the links dataset does not need to be ...
# §3.2.2.2(vi): ... replicated, because partitions of it can be rebuilt ...
# §3.2.2.2(vi): ... efficiently by rerunning a map on blocks of the input file.
# §3.2.2.2(vii): This dataset will typically be ...
# §3.2.2.2(vii): ... much larger than ranks, because each document has ...
# §3.2.2.2(vii): ... many links but only one number as its rank, so ...
# §3.2.2.2(vii): ... recovering it using lineage saves time over systems ...
# §3.2.2.2(vii): ... that checkpoint a program’s entire in-memory state.
#-------------------------------------------------------------------------------
# §3.2.2.3(i): Finally, we can optimize communication in PageRank ...
# §3.2.2.3(i): ... by controlling the partitioning of the RDDs.
# §3.2.2.3(ii): If we specify a partitioning for links (e.g., hash-partition ...
# §3.2.2.3(ii): ... the link lists by URL across nodes), we can ...
# §3.2.2.3(ii): ... partition ranks in the same way and ensure that the ...
# §3.2.2.3(ii): ... join operation between links and ranks ...
# §3.2.2.3(ii): ... requires no communication (as each URL’s rank will be ...
# §3.2.2.3(ii): ... on the same machine as its link list).
# §3.2.2.3(iii): We can also write a custom Partitioner class to group pages ...
# §3.2.2.3(iii): ... that link to each other together (e.g., partition the ...
# §3.2.2.3(iii): ... URLs by domain name).
# §3.2.2.3(iv): Both optimizations can be expressed by ...
# §3.2.2.3(iv): ... calling partitionBy when we define links.
def example_3_2_2_3(context):
    links = context.textFile("...").map().partitionBy(4, myPartFunc).persist()
#===============================================================================
# §4: Representing RDDs
#-------------------------------------------------------------------------------
# §4.1(i): One of the challenges in providing RDDs as an abstraction is ...
# §4.1(i): ... choosing a representation for them that can ...
# §4.1(i): ... track lineage across a wide range of transformations.
# §4.1(ii): Ideally, a system implementing RDDs should provide as rich a set ...
# §4.1(ii): ... of transformation operators as possible (e.g., the ones ...
# §4.1(ii): ... in Table 2), and let users compose them in arbitrary ways.
# §4.1(iii): We propose a simple graph-based representation for RDDs ...
# §4.1(iii): ... that facilitates these goals.
# §4.1(iv): We have used this representation in Spark to support a wide ...
# §4.1(iv): ... range of transformations without adding special logic to the ...
# §4.1(iv): ... scheduler for each one, which greatly simplified the ...
# §4.1(iv): ... system design.
#-------------------------------------------------------------------------------
# §4.2(i): In a nutshell, we propose representing each RDD through a ...
# §4.2(i): ... common interface that exposes five pieces of information: ...
# §4.2(i): ... a set of partitions, which are atomic pieces of the dataset; ...
# §4.2(i): ... a set of dependencies on parent RDDs; ...
# §4.2(i): ... a function for computing the dataset based on its parents; ...
# §4.2(i): ... and metadata about its partitioning scheme ...
# §4.2(i): ... and data placement.
# §4.2(ii): For example, an RDD representing an HDFS file has a partition ...
# §4.2(ii): ... for each block of the file and knows ...
# §4.2(ii): ... which machines each block is on.
# §4.2(iii): Meanwhile, the result of a map on this RDD has ...
# §4.2(iii): ... the same partitions, but applies the map function ...
# §4.2(iii): ... to the parent’s data when computing its elements.
# §4.2(iv): We summarize this interface in Table 3.
#-------------------------------------------------------------------------------
# Table 3: Interface used to represent RDDs in Spark
# Table 3(i): Operation: Meaning
# Table 3(ii):  partitions(): Return a list of Partition objects
# Table 3(iii): preferredLocations(p): ...
# Table 3(iii): ... List nodes where partition p can be accessed faster ...
# Table 3(iii): ... due to data locality
# Table 3(iv):  dependencies(): Return a list of dependencies
# Table 3(v):   iterator(p, parentIters): ...
# Table 3(v):   ... Compute the elements of partition p ...
# Table 3(v):   ... given iterators for its parent partitions
# Table 3(vi):  partitioner(): ...
# Table 3(vi):  ... Return metadata specifying ...
# Table 3(vi):  ... whether the RDD is hash/range partitioned
#-------------------------------------------------------------------------------
# §4.3(i): The most interesting question in designing this interface ...
# §4.3(i): ... is how to represent dependencies between RDDs.
# §4.3(ii): We found it both sufficient and useful to ...
# §4.3(ii): ... classify dependencies into two types: ...
# §4.3(ii): ... narrow dependencies, where each partition of the parent RDD ...
# §4.3(ii): ... is used by at most one partition of the child RDD, ...
# §4.3(ii): ... wide dependencies, where multiple child partitions ...
# §4.3(ii): ... may depend on it.
# §4.3(iii): For example, map leads to a narrow dependency, ...
# §4.3(iii): ... while join leads to to wide dependencies ...
# §4.3(iii): ... (unless the parents are hash-partitioned).
# §4.3(iv): Figure 4 shows other examples.
#-------------------------------------------------------------------------------
# §4.4(i): This distinction is useful for two reasons.
# §4.4(ii): First, narrow dependencies allow for pipelined execution on ...
# §4.4(ii): ... one cluster node, which can compute all the parent partitions.
# §4.4(iii): For example, one can apply a map followed by a filter ...
# §4.4(iii): ... on an element-by-element basis.
# §4.4(iv): In contrast, wide dependencies require data from all ...
# §4.4(iv): ... parent partitions to be available and to be shuffled ...
# §4.4(iv): ... across the nodes using a MapReduce-like operation.
# §4.4(v): Second, recovery after a node failure is more efficient with a ...
# §4.4(v): ... narrow dependency, as only the lost parent partitions need to ...
# §4.4(v): ... be recomputed, and they can be recomputed ...
# §4.4(v): ... in parallel on different nodes.
# §4.4(vi): In contrast, in a lineage graph with wide dependencies, a single ...
# §4.4(vi): ... failed node might cause the loss of some partition from ...
# §4.4(vi): ... all the ancestors of an RDD, requiring a complete re-execution.
#===============================================================================
# §4.5(i): This common interface for RDDs made it possible to implement ...
# §4.5(i): ... most transformations in Spark in less than 20 lines of code.
# §4.5(ii): Indeed, even new Spark users have implemented new ...
# §4.5(ii): ... transformations (e.g., sampling and various types of joins) ...
# §4.5(ii): ... without knowing the details of the scheduler.
# §4.5(iii): We sketch some RDD implementations below.
#-------------------------------------------------------------------------------
# §4.5.1(i): HDFS files: The input RDDs in our samples have been files in HDFS.
# §4.5.1(ii): For these RDDs, partitions returns one partition for each ...
# §4.5.1(ii): ... block of the file (with the block’s offset stored in each ...
# §4.5.1(ii): ... Partition object), preferredLocations gives the nodes the ...
# §4.5.1(ii): ... block is on, and iterator reads the block.
#-------------------------------------------------------------------------------
# §4.5.2(i): map: Calling map on any RDD returns a MappedRDD object.
# §4.5.2(ii): This object has the same partitions and preferred locations ...
# §4.5.2(ii): ... as its parent, but applies the function passed to map ...
# §4.5.2(ii): ... to the parent’s records in its iterator method.
#-------------------------------------------------------------------------------
# §4.5.3(i): union: Calling union on two RDDs returns an RDD ...
# §4.5.3(i): ... whose partitions are the union of those of the parents.
# §4.5.3(ii): Each child partition is computed through a narrow dependency ...
# §4.5.3(ii): ... on the corresponding parent.
#-------------------------------------------------------------------------------
# §4.5.4: sample: Sampling is similar to mapping, except that the RDD ...
# §4.5.4: ... stores a random number generator seed for each partition ...
# §4.5.4: ... to deterministically sample parent records.
#-------------------------------------------------------------------------------
# §4.5.5(i): join: Joining two RDDs may lead to either ...
# §4.5.5(i): ... two narrow dependencies (if they are both hash/range ...
# §4.5.5(i): ... partitioned with the same partitioner), ...
# §4.5.5(i): ... two wide dependencies, or a mix (if one parent has a ...
# §4.5.5(i): ... partitioner and one does not).
# §4.5.5(ii): In either case, the output RDD has a partitioner (either one ...
# §4.5.5(ii): ... inherited from the parents or a default hash partitioner).
#===============================================================================
# §5: Implementation
#-------------------------------------------------------------------------------
# §5.0.1(i): We have implemented Spark in about 14,000 lines of Scala.
# §5.0.1(ii): The system runs over the Mesos cluster manager ...
# §5.0.1(ii): ... [17], allowing it to share resources with Hadoop, ...
# §5.0.1(ii): ... MPI and other applications.
# §5.0.1(iii): Each Spark program runs as a separate Mesos application, ...
# §5.0.1(iii): ... with its own driver (master) and workers, and resource ...
# §5.0.1(iii): ... sharing between these applications is handled by Mesos.
#-------------------------------------------------------------------------------
# §5.0.2: Spark can read data from any Hadoop input source (e.g., HDFS ...
# §5.0.2: ... or HBase) using Hadoop’s existing input plugin APIs, and ...
# §5.0.2: ... runs on an unmodified version of Scala.
#-------------------------------------------------------------------------------
# §5.0.3: We now sketch several of the technically interesting parts of ...
# §5.0.3: ... the system: our job scheduler (§5.1), our ...
# §5.0.3: ... Spark interpreter allowing interactive use (§5.2), ...
# §5.0.3: ... memory management (§5.3), and support for ...
# §5.0.3: ... checkpointing (§5.4).
#===============================================================================
# §5.1: Job Scheduling
#-------------------------------------------------------------------------------
# §5.1.1: Spark’s scheduler uses our representation of RDDs, ...
# §5.1.1: ... described in Section 4.
#-------------------------------------------------------------------------------
# §5.1.2(i): Overall, our scheduler is similar to Dryad’s [19], ...
# §5.1.2(i): ... but it additionally takes into account ...
# §5.1.2(i): ... which partitions of persistent RDDs are available in memory.
# §5.1.2(ii): Whenever a user runs an action (e.g., count or save) on ...
# §5.1.2(ii): ... an RDD, the scheduler examines that RDD’s lineage graph to ...
# §5.1.2(ii): ... build a DAG of stages to execute, as illustrated in Figure 5.
# §5.1.2(iii): Each stage contains as many pipelined transformations ...
# §5.1.2(iii): ... with narrow dependencies as possible.
# §5.1.2(iv): The boundaries of the stages are the shuffle operations ...
# §5.1.2(iv): ... required for wide dependencies, or any already computed ...
# §5.1.2(iv): ... partitions that can short-circuit the ...
# §5.1.2(iv): ... computation of a parent RDD.
# §5.1.2(v): The scheduler then launches tasks to compute missing partitions ...
# §5.1.2(v): ... from each stage until it has computed the target RDD.
#-------------------------------------------------------------------------------
# §5.1.2(i): Our scheduler assigns tasks to machines ...
# §5.1.2(i): ... based on data locality using delay scheduling [32].
# §5.1.2(ii): If a task needs to process a partition that is available ...
# §5.1.2(ii): ... in memory on a node, we send it to that node.
# §5.1.2(iii): Otherwise, if a task processes a partition for which the ...
# §5.1.2(iii): ... containing RDD provides preferred locations (e.g., an ...
# §5.1.2(iii): ... HDFS file), we send it to those.
#-------------------------------------------------------------------------------
# §5.1.3: For wide dependencies (i.e., shuffle dependencies), we currently ...
# §5.1.3: ... materialize intermediate records on the nodes holding parent ...
# §5.1.3: ... partitions to simplify fault recovery, much like MapReduce ...
# §5.1.3: ... materializes map outputs.
#-------------------------------------------------------------------------------
# §5.1.4(i): If a task fails, we re-run it on another node ...
# §5.1.4(i): ... as long as its stage’s parents are still available.
# §5.1.4(ii): If some stages have become unavailable (e.g., because an ...
# §5.1.4(ii): ... output from the “map side” of a shuffle was lost), we ...
# §5.1.4(ii): ... resubmit tasks to compute the missing partitions in parallel.
# §5.1.4(iii): We do not yet tolerate scheduler failures, though ...
# §5.1.4(iii): ... replicating the RDD lineage graph would be straightforward.
#-------------------------------------------------------------------------------
# §5.1.5(i): Finally, although all computations in Spark currently run ...
# §5.1.5(i): ... in response to actions called in the driver program, ...
# §5.1.5(i): ... we are also experimenting with letting tasks on the cluster ...
# §5.1.5(i): ... (e.g., maps) call the lookup operation, which provides ...
# §5.1.5(i): ... random access to elements of hash-partitioned RDDs by key.
# §5.1.5(ii): In this case, tasks would need to tell the scheduler ...
# §5.1.5(ii): ... to compute the required partition if it is missing.
#===============================================================================
# §5.2: Interpreter Integration
#-------------------------------------------------------------------------------
# §5.2.1(i): Scala includes an interactive shell ...
# §5.2.1(i): ... similar to those of Ruby and Python.
# §5.2.1(ii): Given the low latencies attained with in-memory data, ...
# §5.2.1(ii): ... we wanted to let users run Spark interactively ...
# §5.2.1(ii): ... from the interpreter to query big datasets.
#-------------------------------------------------------------------------------
# §5.2.2(i): The Scala interpreter normally operates by compiling a class ...
# §5.2.2(i): ... for each line typed by the user, loading it into the JVM, ...
# §5.2.2(i): ... and invoking a function on it.
# §5.2.2(ii): This class includes a singleton object that contains ...
# §5.2.2(ii): ... the variables or functions on that line and ...
# §5.2.2(ii): ... runs the line’s code in an initialize method.
#-------------------------------------------------------------------------------
# §5.2.2(iii): For example, if the user types var x = 5 followed by ...
# §5.2.2(iii): ... println(x), the interpreter defines a class called Line1 ...
# §5.2.2(iii): ... containing x and causes the second line to ...
# §5.2.2(iii): ... compile to println(Line1.getInstance().x).
#-------------------------------------------------------------------------------
# §5.2.3: We made two changes to the interpreter in Spark:
#-------------------------------------------------------------------------------
# §5.2.3.1: Class shipping: To let the worker nodes fetch the bytecode ...
# §5.2.3.1: ... for the classes created on each line, ...
# §5.2.3.1: ... we made the interpreter serve these classes over HTTP.
#-------------------------------------------------------------------------------
# §5.2.3.2(i): Modified code generation: Normally, the singleton object ...
# §5.2.3.2(i): ... created for each line of code is accessed through ...
# §5.2.3.2(i): ... a static method on its corresponding class.
# §5.2.3.2(ii): This means that when we serialize a closure referencing a ...
# §5.2.3.2(ii): ... variable defined on a previous line, such as Line1.x ...
# §5.2.3.2(ii): ... in the example above, Java will not trace through the ...
# §5.2.3.2(ii): ... object graph to ship the Line1 instance wrapping around x.
# §5.2.3.2(iii): Therefore, the worker nodes will not receive x.
# §5.2.3.2(iv): We modified the code generation logic ...
# §5.2.3.2(iv): ... to reference the instance of each line object directly.
#-------------------------------------------------------------------------------
# §5.2.4: Figure 6 shows how the interpreter translates a set of lines ...
# §5.2.4: ... typed by the user to Java objects after our changes.
#-------------------------------------------------------------------------------
# §5.2.5(i): We found the Spark interpreter to be useful in processing ...
# §5.2.5(i): ... large traces obtained as part of our research and ...
# §5.2.5(i): ... exploring datasets stored in HDFS.
# §5.2.5(i): We also plan to use ...
# §5.2.5(i): ... to run higher-level query languages interactively, e.g., SQL.
#===============================================================================
# §5.3: Memory Management
#-------------------------------------------------------------------------------
# §5.3.1(i): Spark provides three options for storage of persistent RDDs: ...
# §5.3.1(i): ... in-memory storage as deserialized Java objects, ...
# §5.3.1(i): ... in-memory storage as serialized data, ...
# §5.3.1(i): ... and on-disk storage.
# §5.3.1(ii): The first option provides the fastest performance, ...
# §5.3.1(ii): ... because the Java VM can access each RDD element natively.
# §5.3.1(iii): The second option lets users choose a more memory-efficient ...
# §5.3.1(iii): ... representation than Java object graphs ...
# §5.3.1(iii): ... when space is limited, at the cost of lower performance.
# §5.3.1(iv): The third option is useful for RDDs that are too large ...
# §5.3.1(iv): ... to keep in RAM but costly to recompute on each use.
#-------------------------------------------------------------------------------
# §5.3.2(i): To manage the limited memory available, ...
# §5.3.2(i): ... we use an LRU eviction policy at the level of RDDs.
# §5.3.2(ii): When a new RDD partition is computed but there ...
# §5.3.2(ii): ... is not enough space to store it, we ...
# §5.3.2(ii): ... evict a partition from the least recently accessed RDD, ...
# §5.3.2(ii): ... unless this is the same RDD as the one with the new partition.
# §5.3.2(iii): In that case, we keep the old partition in memory ...
# §5.3.2(iii): ... to prevent cycling partitions from the same RDD in and out.
# §5.3.2(iv): This is important because most operations will run tasks ...
# §5.3.2(iv): ... over an entire RDD, so it is quite likely that the ...
# §5.3.2(iv): ... partition already in memory will be needed in the future.
# §5.3.2(v): We found this default policy to work well in all our ...
# §5.3.2(v): ... applications so far, but we also give users further ...
# §5.3.2(v): ... control via a “persistence priority” for each RDD.
#-------------------------------------------------------------------------------
# §5.3.3(i): Finally, each instance of Spark on a cluster ...
# §5.3.3(i): ... currently has its own separate memory space.
# §5.3.3(ii): In future work, we plan to investigate sharing RDDs ...
# §5.3.3(ii): ... across instances of Spark through a unified memory manager.
#===============================================================================
# §5.4: Support for Checkpointing
#-------------------------------------------------------------------------------
# §5.4.1(i): Although lineage can always be used to recover RDDs ...
# §5.4.1(i): ... after a failure, such recovery may be time-consuming ...
# §5.4.1(i): ... for RDDs with long l-ineage chains.
# §5.4.1(ii): Thus, it can be helpful to checkpoint some RDDs to stable storage.
#-------------------------------------------------------------------------------
# §5.4.2(i): In general, checkpointing is useful for RDDs with long ...
# §5.4.2(i): ... lineage graphs containing wide dependencies, such as the ...
# §5.4.2(i): ... rank datasets in our PageRank example (§3.2.2).
# §5.4.2(ii): In these cases, a node failure in the cluster may result in ...
# §5.4.2(ii): ... the loss of some slice of data from each parent RDD, ...
# §5.4.2(ii): ... requiring a full recomputation [20].
# §5.4.2(iii): In contrast, for RDDs with narrow dependencies on data in ...
# §5.4.2(iii): ... stable storage, such as the points in our ...
# §5.4.2(iii): ... logistic regression example (§3.2.1) and the link lists ...
# §5.4.2(iii): ... in PageRank, checkpointing may never be worthwhile.
# §5.4.2(iv): If a node fails, lost partitions from these RDDs can be ...
# §5.4.2(iv): ... recomputed in parallel on other nodes, at a ...
# §5.4.2(iv): ... fraction of the cost of replicating the whole RDD.
#-------------------------------------------------------------------------------
# §5.4.3(i): Spark currently provides an API for checkpointing (a ...
# §5.4.3(i): ... REPLICATE flag to persist), but leaves the decision of ...
# §5.4.3(i): ... which data to checkpoint to the user.
# §5.4.3(ii): However, we are also investigating how to ...
# §5.4.3(ii): ... perform automatic checkpointing.
# §5.4.3(iii): Because our scheduler knows the size of each dataset ...
# §5.4.3(iii): ... as well as the time it took to first compute it, ...
# §5.4.3(iii): ... it should be able to select an optimal set of RDDs ...
# §5.4.3(iii): ... to checkpoint to minimize system recovery time [30].
#-------------------------------------------------------------------------------
# §5.4.4(i): Finally, note that the read-only nature of RDDs ...
# §5.4.4(i): ... makes them simpler to checkpoint than general shared memory.
# §5.4.4(ii): Because consistency is not a concern, RDDs ...
# §5.4.4(ii): ... can be written out in the background without requiring ...
# §5.4.4(ii): ... program pauses or distributed snapshot schemes.
#===============================================================================
# §6: Evaluation
#-------------------------------------------------------------------------------
def word_count(context):
    texts = ["Hello Spark", "Hello RDD", "Hello Scala"]
    lines = context.parallelize(texts)
    words = lines.flatMap(lambda line: line.split(" "))
    word_pairs = words.map(lambda word: (word, 1))
    word_count = word_pairs.reduceByKey(lambda total, value: total + value)
    pprint(word_count.collect())
#-------------------------------------------------------------------------------
def fruits(context):
    data = [
        ("apple", 1),
        ("banana", 2),
        ("apple", 3),
        ("orange", 4),
        ("banana", 5)]
    fruits = context.parallelize(data)
    counts = fruits.reduceByKey(lambda total, value: total + value)
    pprint(counts.collect())
#-------------------------------------------------------------------------------
def numbers(context):
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    numbers = context.parallelize(data)
    doubled = numbers.map(lambda n: n * 2)
    filtered = doubled.filter(lambda n: n > 10)
    pprint(filtered.collect())
    sum_of_numbers = numbers.reduce(lambda total, value: total + value)
    pprint(sum_of_numbers)
#-------------------------------------------------------------------------------
def sand_box(context):
    data = [1, 2, 3, 4, 5, 6]
    rdd = context.parallelize(data)
    evens = rdd.filter(lambda x: x % 2 == 0)
    squares = evens.map(lambda x: x * x)
    sum = squares.reduce(lambda x, y: x + y)
    rdd1 = context.parallelize((("a", 1), ("b", 2), ("a", 3)))
    rdd2 = context.parallelize((("a", "x"), ("b", "y")))
    grouped = rdd1.groupByKey()
    pprint(grouped.mapValues(lambda vs: list(vs)).collect())
    joined = rdd1.join(rdd2)
    pprint(joined.collect())
    base = context.parallelize(list(range(1, 11)))
    filtered = base.filter(lambda x: x % 2 == 0)
    mapped = filtered.map(lambda x: x * 10)
    mapped.persist()
    mapped.count()
    pprint(mapped.collect())
#===============================================================================
# §7: Discussion
# §8: Related Work
#-------------------------------------------------------------------------------
data = list(range(1, 17))
pairs1 = [(x % 2, x) for x in range(4)]
pairs2 = [(x % 2, x * 2) for x in range(4)]
tests = [
  ("rdd",       lambda: context.parallelize(data))
, ("rdd_1",     lambda: rdd.map(lambda x: x * 2))
, ("rdd_2",     lambda: rdd_1.filter(lambda x: x < 10))
, ("rdd_3",     lambda: rdd_2.flatMap(lambda x: [x, -x]))
, ("rdd_4",     lambda: rdd_3.sample(False, 0.5, seed=53))
, ("rdd_A",     lambda: context.parallelize(pairs1))
, ("rdd_B",     lambda: context.parallelize(pairs2))
, (None,        lambda: [ (k, list(vs))
                          for k, vs in rdd_A.groupByKey().collect()
                        ])
, ("rdd_G",     lambda: rdd_A.groupByKey().mapValues(lambda vs: list(vs)))
, ("rdd_R",     lambda: rdd_A.reduceByKey(lambda total, count: total + count))
, ("rdd_U",     lambda: rdd_A.union(rdd_B))
, ("rdd_J",     lambda: rdd_A.join(rdd_B))
, (None,        lambda: [ (k, [list(vv) for vv in vs])
                          for k, vs in rdd_A.cogroup(rdd_B).collect()
                        ])
, ("rdd_CG",    lambda: rdd_A.cogroup(rdd_B)
                             .mapValues(lambda vs: [list(vv) for vv in vs]))
, ("rdd_CP",    lambda: rdd_A.cartesian(rdd_B)) # .crossProduct(rdd_B)
, ("rdd_MV",    lambda: rdd_A.mapValues(lambda v: v * 100))
, ("rdd_S",     lambda: rdd_A.sortBy(lambda k: k,
                                ascending=True,
                                numPartitions=None)
  )
, ("rdd_PB",    lambda: rdd_A.partitionBy(2, lambda k: hash(k)))
, (None,        lambda: rdd_A.count())
, ("rdd_nums",  lambda: rdd.map(lambda x: x))
, (None,        lambda: rdd_nums.reduce(lambda total, count: total + count))
, (None,        lambda: rdd_A.lookup(1))
]
#===============================================================================
# §9: Conclusion
#-------------------------------------------------------------------------------
cluster = [Machine(n) for n in range(N_MACHINES)]
for test in [ test_2_2_0_2
            , example_2_2_1_1
            , example_2_2_1_2
            , example_2_2_1_3
            , example_3_2_1
            , example_3_2_2
            , word_count
            , fruits
            , numbers
            , sand_box
            ]:
    for context in (spark, spock): # (spock,)
        test(context)
    print()
pprint(cluster)
#-------------------------------------------------------------------------------
cluster = [Machine(n) for n in range(N_MACHINES)]
for context in (spark, spock): # (spock,)
    for test in tests:
        variable = test[0]
        function = test[1]
        value = function()
        if (variable):
            globals()[variable] = value
            print(f"{variable}: {pformat(value.collect())}")
        else: pprint(value)
    print()
pprint(cluster)
#===============================================================================
