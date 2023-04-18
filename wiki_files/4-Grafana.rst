Grafana
*******

----

To deploy Dashboards with our Data we will be using Grafana local instance instead of the cloud version, mostly due do network constraints.

The requirements/parameters are:

+ Connection to FEUP VPN
+ Address: 10.227.211.12
+ Port: 3000
+ Full Address: :code:`10.227.211.12:3000//login`
+ Username: admin
+ Password: digi2-gpu

|


Adding PostgreSQL DataSource
............................

Creating Dashboards require data, therefore one must previously add the data source. To accomplish that:



(1) Front Page
++++++++++++++
ℹ️ This is the main grafana front page. 

.. image:: https://user-images.githubusercontent.com/98216516/232913457-4f729358-b0ad-4647-970a-83906f454017.PNG

  
(2) Access DataSources
++++++++++++++++++++++       
ℹ️ The Left tab allow us to access our Data Sources list, under the Configuration menu.

.. image:: https://user-images.githubusercontent.com/98216516/232913578-e1d552e9-7e61-4042-965e-764883d4ec1a.PNG


(3) Adding New DataSource
+++++++++++++++++++++++++
ℹ️ This page allow us to manage the added data sources and add new ones.
            
.. image:: https://user-images.githubusercontent.com/98216516/232913960-fbb36b45-c4ed-4966-a144-bd787cd8e262.PNG

  
(4) Search Available DataSources
++++++++++++++++++++++++++++++++
ℹ️ This search page allow us to choose the supported Data Sources by Grafana. For the current application, we will be using the **PostgreSQL**.
        
.. image:: https://user-images.githubusercontent.com/98216516/232913985-17b6b063-164f-4e4b-987f-d5a41b3fd8d4.PNG

   
(5) DataSource Settings
+++++++++++++++++++++++
ℹ️ The main settings to add/change:
            
+ Data Source Name
+ PostgreSQL Connection
    - host: :code:`db.fe.up.pt`
    - database name
    - username
    - password
    - TLS/SSL Mode **disabled**
            
Then, after clicking the :code:`Save & Test` button, the data source is ready to be used (if the message "Database Connection OK" appears).
 
.. image:: https://user-images.githubusercontent.com/98216516/232914016-2ecd864d-d68c-4f04-bd1f-86d8c2cac783.PNG

  
(6) Checking DataSources List
+++++++++++++++++++++++++++++
ℹ️ If the Data Source was successfully added it should be visible in the Data Sources List (under the configuration menu on the left tab)
        
.. image:: https://user-images.githubusercontent.com/98216516/232914035-4c45d129-abb4-4434-b630-3df36e99eadf.PNG


|

|

The full steps are portrayed below:

.. image:: https://user-images.githubusercontent.com/98216516/232914067-3a10b21c-d0e1-4206-93e8-d98ac344f601.gif












|


Exploring the Data Source
.........................


Before creating one dashboard, it could be useful to check if Grafana is being able to extract the data from our DataBase.



(1)Access to Explorer
+++++++++++++++++++++
ℹ️ We explore the Data Source by clicking the **Explore** button.
        
.. image:: https://user-images.githubusercontent.com/98216516/232914380-48e4abdb-2b16-4212-bfbf-4b45c8ce7e03.PNG
 
(2)Testing Query
++++++++++++++++
ℹ️ To execute some query, follow the steps:
            
+ Select the desired output format (table, time series, etc);
+ Build the query with the Query Editor
            
Example: query the database and display the column "time_start" values
        
.. image:: https://user-images.githubusercontent.com/98216516/232914433-65c1241f-ce00-403a-ba80-f45b8479e025.PNG
   
|

Solving "No Data"
+++++++++++++++++

❌ No data is retrieved. This usually happens due to the fact that Grafana usually sets automatically the highest search path. The workaround for this is to **Edit** the Query and add the schema.
            
Example: the table **"WELD_SAMPLES"** would be replaced by **"DINASORE"."WELD_SAMPLES"** being "DINASORE" our schema.

|
        
By accessing the :code:`code` tab we can **edit** the Queries:
        
.. image:: https://user-images.githubusercontent.com/98216516/232914483-d8716535-7e4f-4acc-8cc7-5175f2f7d944.PNG


|
        
And, after adding the schema it results:
        
.. image:: https://user-images.githubusercontent.com/98216516/232914519-5c38c13e-8461-41e0-9fc4-53bc6efc4699.PNG

|

|

Creating Dashboard
..................


(1)Selecting DataSource
+++++++++++++++++++++++
ℹ️ The button "Build a Dashboard" quickly selects the desired data source to be used on the dashboard we want to create.

.. image:: https://user-images.githubusercontent.com/98216516/232915357-86441d89-2e30-4f24-878f-c2f9d40570ac.PNG

(2)Adding Panel
+++++++++++++++
ℹ️ Dashboards may have a variety of elements. To start adding the first element, we can choose "Add a new Panel".
        
.. image:: https://user-images.githubusercontent.com/98216516/232915420-8df9207d-1e2e-4313-ac06-43444654e2ac.PNG

   
(3)Building Queries
+++++++++++++++++++
ℹ️ This page allow us to configure our dashboard element. As for the data to be visualized, we build queries with the Query Editor which will provide the data.
            
.. image:: https://user-images.githubusercontent.com/98216516/232915462-c3a6de9d-6248-4a47-b423-cc02b8f2889e.png

  
(4)Query Example
+++++++++++++++++++
ℹ️ For this example, the objective is to plot each row average force.
        
|
        
Consider that we have the following table structure:
        
+-----+------------+
|  id | force      |
+=====+============+
|  1  |  {1,2,3}   |
+-----+------------+
|  2  |  {3,3,6}   |
+-----+------------+
|  3  |  {4,6,5}   |
+-----+------------+
| ... |  ...       |
+-----+------------+

Then, for each row the average would be:
        
+-----+-----------+
|  id | avg_force |
+=====+===========+
|  1  |  2        |
+-----+-----------+
|  2  |  4        |
+-----+-----------+
|  3  |  5        |
+-----+-----------+
| ... |  ...      |
+-----+-----------+

Thefore, we would like to plot x = {1, 2, 3, ...} and y = {2, 4, 5, ...}.
        
        
With the following SQL it is possible to accomplish that:
        
```sql
SELECT id AS "time", AVG(val) AS "AverageForce" FROM 
(SELECT id, UNNEST(force) AS val FROM "DINASORE"."WELD_SAMPLES" ) 
subquery GROUP BY id ORDER BY id LIMIT 50;
```

        
        
        
Since this code has more complexity, it is preferred to write it on the code Editor instead of using the Query Editor/Builder.
        
|
        
Limiting to just 50 welding samples:
        
.. image:: https://user-images.githubusercontent.com/98216516/232915511-1af8a3e0-80d1-4d83-a0ca-164ed2cb5503.PNG
       
|
        
With 5000 welding samples (change to :code:`LIMIT 5000`):

.. image:: https://user-images.githubusercontent.com/98216516/232915534-2d7cac17-e10c-4be1-b981-f68d071dbebc.PNG



  
(5)Saving the Dashboard
+++++++++++++++++++++++
ℹ️ After adding our queries and configuring our Dashboard we apply the changes to save it.
        
|

.. image:: https://user-images.githubusercontent.com/98216516/232915560-768e68d8-1fce-4767-bb6a-70cf110b3667.PNG
      
|
        
Checking our panel:
        
.. image:: https://user-images.githubusercontent.com/98216516/232915575-cf8a40b8-1436-4cf0-9ec5-e6ead81ae74a.PNG
       
|
        
Saving the Dashboard:
        
.. image:: https://user-images.githubusercontent.com/98216516/232915591-9024102b-d472-4dc1-b2c4-a3c47c914cb2.PNG
    
        

  
(6)Multiple Queries
ℹ️ It is also possible to have multiple queries on the same dashboard element.
        
|
        
.. image:: https://user-images.githubusercontent.com/98216516/232915611-796e1c3a-2cb5-4f97-8f60-d2ebd254349b.PNG
     
|
        
The queries used above are:
        
```sql
SELECT id AS "time", AVG(val) AS "AverageForce" FROM 
(SELECT id, UNNEST(force) AS val FROM "DINASORE"."WELD_SAMPLES" ) 
subquery GROUP BY id ORDER BY id LIMIT 5000;


SELECT id AS "time", AVG(val) AS "AverangeAngularVelocity" FROM 
(SELECT id, UNNEST(angular_velocity) AS val FROM "DINASORE"."WELD_SAMPLES" ) 
subquery GROUP BY id ORDER BY id LIMIT 5000;


SELECT id AS "time", AVG(val) AS "AverangeDisplacement" FROM 
(SELECT id, UNNEST(displacement) AS val FROM "DINASORE"."WELD_SAMPLES" ) 
subquery GROUP BY id ORDER BY id LIMIT 5000;
```


|
