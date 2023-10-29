# Questions
Please answer the following questions with a few sentences each in preparation for your interview. If you can’t answer a question, leave them out (don’t just google for an answer).

#### 1- How do you estimate the runtime behavior of your implementation in terms of CPU usage and memory consumption?
- Considering the complexity of CPU operations in our code by thinking about BigO of implemented algorithms
- Using memory profilers (I don't have experience working with these tools)
- Using profiling tools to find out the bottlenecks. For example, I use ``Silk`` for profiling our endpoints and methods
- Monitoring the CPU and memory usage by setting up tools like ``Grafana``
- Using loaders like ``Locust`` we are using for test our endpoints


#### 2- How do you approach designing and architecting large-scale Python applications, and what tools or techniques do you use to ensure scalability, maintainability, and performance?
- Understanding the functional and non-functional requirements is the most important step
- Estimating the potential loads
- Writing maintainable code by following standards, best practices, reviews, refactoring, and etc
- Using microservice architecture to provide high scalability, availability, maintainability, and fast deployment
- Selecting the right database system RDBMS or NoSQL
- Using mechanisms like caching, async tasks, query optimizations, and load balancing for performance and availability

#### 3- Can you describe your experience working with any Python web frameworks, such as Flask or Django, and how you have used third-party tools or libraries to enhance their functionality?
- This is 6 years that I am participating in developing web application by Django
- I don't have experience with Flask
- For example, I use DRF as a third party library to create RESTFul APIs. And I used Django Elasticsearch DSL library to integrate Elasticsearch with Django

#### 4- Can you discuss your experience with authentication and authorization in API design, and how you have implemented these features in Python?
- In Django, I have experience with ``JWT`` as a secure and stateless authentication mechanism
- The authorization comes after authentication where we check whether the user has permission on the requested operation
- I have experience with the RBAC access control concept as we are currently using 

#### 5- What are the pros and cons of deploying applications as a container (e.g. Docker)?

We are currently using containers, based on my experience:

Pros:
- it enables us to make sure that the application works on different environments like development, stage, and production 
- it ensures that our dependencies doesn't have conflict with the system and other containers 
- it enables us to scale up the whole or part of our application to have multiple instances to deal with high load
- reducing the deployment time as we already have the production ready image of our application
- when we containerized an application it works on any platform that provides a docker engin
- helping CI/CD pipelines
- a good fit for microservice architecture
- very straightforward to roll back to the previous version 

Cons:

- adding overhead to team to deal with containerizing the application and maintaining the image repository
- complexity in the communication between multiple containers


#### 6- Suppose you need to continuously roll out an application to several stations in multiple remote locations in different time zones and sometimes unstable/slow internet connections. Service continuity and stability are paramount. Each on-site location has a central server available. How would you make sure that you can roll out updated versions of the application in a timely fashion while interrupting the service as shortly as possible?

- by containerizing the application we are sure that new updates will work on every central server
- make sure that the new update is deployed without issue by leveraging stage servers
- having multiple images repositories close to the central servers can reduce the network delay
- keep our images as small as possible
- using orchestration like kubernetes or docker swarm for rolling updates and fast roll back in case of having issues
- using load balancers to distribute traffic over multiple server (instances)
- schedule update for each time zone in the lower traffics
- monitoring the new updates to make sure that everything is working well


#### 7- How do you optimize queries in a relational database, such as PostgreSQL or MySQL? Can you discuss techniques such as indexing, query planning, or query optimization?
 
- using indexes for columns which are frequently used in queries ``Where`` clauses to improve the read operations
- fetch only the necessary attributes instead of all attributes
- avoid ``N+1`` queries by fetching the relations records in the main query. In Django, we can use ``prefetch_related`` and ``select_related``
- using profilers to identify the slow queries. I use ``Silk`` in this case
- using query tools like ``PgAdmin`` to execute the actual SQL query and its plan 
- use the joins and aggregation functions very carefully
- sometimes denormalization would improv the performance for read operations
- using bulk queries to reduce the number of queries. For example, we can use ``bulk_create`` or ``bulk_update`` in Django
- using pagination if it is possible (limiting the number of records)
- using caching to reduce the DB hits

Indexing: indexing is a technique where RDBMS create a new structures, like B-tree, to point the records in a table such that accessing to the indexed column is fast since the RDBMS doesn't have to scan whole table

Query Planning: Is a technique to see the steps of execution of a SQL query

Query Optimization: Is the process of rewriting a query to make is faster


#### 8- How does the Toniebox work and what’s needed for a successful interaction with Tonies? If you were to implement a similar product, what would be some of the system design considerations and challenges you have to keep in mind.

I watched a couple of video explaining Tonies and Toniebox. So based on my observation I would say:

- The Toniebox, as a server, interacts with Tonies, as clients, via a Wi-Fi connection.
- Once a Tonie (client) is connected to the Toniebox (server), it sends its own content (an audio file here) to the server and then the server forwards the content to a speaker
- It seems that there is a mechanism to make sure that only one Tonie can connect at the same time. There is a magnet that holds the Tonie and somehow enables that Tonie to connect to the Toniebox and send the audio file
- The Tonibox receives the settings and updates by connecting to a server via internet connection
- Having reliable communication between Tonie and Tnoiebox is the most important feature since it is the core value for users to play audios
- Having a mechanism to update the middleware of these devices is important
- I saw that when a Tonie is detached from the Toniebox, while an audio is playing, after attaching again the audio was resumed which is very nice and complicate to implement. So maybe it is stored in the Tonie to know the last state and when it is connected again the state is resumed (I am just guessing!)
- As it is possible to upload custom audios, the security of these devices is so critical to make sure that an arbitrary audio from a malicious user is not uploaded
- As the Tonieboxes are connecting to the servers to get updates and settings we should make sure that we are providing high available and performance service
- Authentication of Tonies by the Toniebox could be challenging
