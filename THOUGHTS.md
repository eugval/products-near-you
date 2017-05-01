1. How would your design change if the data was not static (i.e updated frequently
during the day)?

In the current design, the data are read from the csv files on startup once, and
then kept in a memory cache to speed up the search.

If the data was dynamic and the csv files where changing throughout the day,
two things to think about would be (1) how often do we want/need those changes
to be available to the clients, and (2) how much code refactoring overhead can
we afford.

In the case where we do not need the data to be readily available, we could simply
alter the design so that the setup_cache function is called periodically. This can be
easily set up through the timeout option in the cached decorator
(cf. https://pythonhosted.org/Flask-Cache/).  The data should be reloaded into the
cache in moments of low traffic, thereby making the new entries available while not
disrupting the service.

One thing to keep an eye on if the database keeps expanding indefinitely is
that our cached data might become very memory expensive. At that point, depending on
the resources that we have available, it might become counterproductive to cache all
the data the way we have been.

Also, while implementing the write and read functionalities in this altered approach
we need to be careful not to allow any harmful race conditions to occur, adding
mutex and lock functionality where appropriate.

If the new data needs to be readily available however, such an approach is not as reasonable.
The setup_cache function is expensive and should not be called regularly or there might be
non-negligible disruptions to the service.

Given the above considerations, in the specified scenario it is probably a better
path to move onto an SQL (or noSQL, such as MongoDB) solution altogether. Doing
this as soon as possible would minimise the code refactoring overhead, while making
the system more maintainable and expandable (as it is an approach that fits all cases).
In this design, the data will be stored in an SQL database which will handle all
the lower level optimisations as well as prevent all race conditions. Optimising our
search might still turn out to be necessary, but would probably take different forms
than what we are using here. One approach would be rewriting the relevant functions
with simple sql queries to get the data and then do some profiling to figure out
if and where any optimisations would be needed.

2. Do you think your design can handle 1000 concurrent requests per second? If not, what
would you change

Using our profiling script (run_with_profiler.py), in our system a search
request takes about 0.6 seconds. This seems acceptable, but is nevertheless  
insufficient to run 1000 concurrent requests per second, as flask's app.run is a
single synchronous process.

Even if we managed to increase the efficiency of our search even more through some
clever search optimisations with perhaps the use an SQL solution it seems unlikely that
we will reach a processing time that is small enough to handle this load.

In order to make the app scalable to this extent, we need to somehow parallelise the
computation.

A quick and dirty solution to achieve that under the current conditions and with minimal
effort is the following:
Have different server instances running, listening on to different ports. Then,
on the client we have each request be sent to one of these instances at random,
thereby effectively splitting the requests into many concurrent processes. These
then can be safely parallelised, splitting the load between them. This would work
because all our data are static and all the requests are completely independent
and not affecting the system in any way. Obviously, this is a very
bad practice that should not be used by anyone, as it would make the extendability
and maintainability of the app reach negative heights.

A probably better approach would then be to use some tool such as Gunicorn that
is designed for such a task and is able to handle multiple concurrent processes.
The requests would then be split between multiple worker processes and threads,
thereby distributing the load and making the app scalable to the extent that we need.
