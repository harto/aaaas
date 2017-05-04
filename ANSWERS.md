Answers
=======

How would you measure the performance of your service?
------------------------------------------------------

I'd use a tool like `ab` with a variety of concurrency settings, which would
provide timings for different load scenarios.

What are some strategies you would employ to make your service more scalable?
-----------------------------------------------------------------------------

 - set long-lived cache headers
 - use a CDN
 - use a load-balancer to distribute requests between multiple API servers
 - run multiple processes per server

How would your design change if you needed to store the uploaded images?
------------------------------------------------------------------------

I'd consider some kind of background/worker process to move uploaded images from
individual servers into shared storage (e.g. S3) at the end of each upload
request.

What are the cost factors of your scaling choices? Which parts of your solution would grow in cost the fastest?
---------------------------------------------------------------------------------------------------------------

I would expect that API servers and network bandwidth would incur the greatest
costs. Persisting uploaded images would incur additional cost, but storage is
cheap relative to CPU.

Where are your critical points of failure and how would you mitigate them?
--------------------------------------------------------------------------

In the initial implementation:

 - excessive resource consumption from processing huge/malformed images
   (mitigated by limiting upload size)

 - single point of failure if Python process or server crashes (mitigate by
   adding additional API servers for redundancy, per scaled-out version)

In a persisted-images implementation:

 - network failure/interruptions while persisting images to permanent storage
   (mitigate by retrying failed persistence operations)

 - primary storage failure (mitigate by keeping regular backups in a separate
   AZ / datacenter)

How given a change to the algorithm what issues do you foresee when upgrading your scaled-out solution?
-------------------------------------------------------------------------------------------------------

Clients could receive different responses for the same request during the
upgrade rollout.

If you wanted to migrate your scaled-out solution to another cloud provider (with comparable offerings but different API’s) how would you envision this happening? How would deal with data consistency during the transition and rollbacks in the event of failures?
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

One solution might be to send requests to both service providers during the
transition. I.e. introduce a top-level reverse proxy that forwards each request
to both the old and new service simultaneously. The responses could be compared
to ensure consistency between old & new providers, and the response from the old
provider would be returned to the user. Once confident that everything is
working, DNS records can be updated to point traffic directly at the new
provider.
