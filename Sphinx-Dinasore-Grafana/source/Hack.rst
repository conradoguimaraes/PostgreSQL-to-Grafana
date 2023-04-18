Hackathon
=========

.. contents:: On this page
   :local:
   :backlinks: none


Database
********

----


The database to be used will be the `PostgreSQL <https://db.fe.up.pt/phppgadmin/>`_. The main connection parameters:

+ database name
+ username
+ password
+ host ('db.fe.up.pt')
+ port (5432)

The data that we want to store in this database has the JSON file format with the following structure:

.. literalinclude:: _static/codes/weld_sample.json
       :language: python
       :linenos:
   
Considering each field corresponding to one column in the database table, the SQL statement (in python string format) below easly creates the table (*WELD_SAMPLES*) with the required columns and data types:


.. tabs::
   
   .. tab:: Standard Format

        .. literalinclude:: _static/codes/sqlstat.sql
               :language: sql
               :linenos:
  
  
   .. tab:: Python String Format

        .. literalinclude:: _static/codes/sqlstat.py
               :language: python
               :linenos:
       

|

Therefore, to insert the JSON welding sample, the SQL statement (in python string format) would be:

.. tabs::
   
   .. tab:: Standard Format

        .. literalinclude:: _static/codes/sqlstat2.sql
               :language: sql
               :linenos:
  
  
   .. tab:: Python String Format

        .. literalinclude:: _static/codes/sqlstat2.py
               :language: python
               :linenos:
               


|


The following Code Example has functions to 

+ delete the DB Schema 
+ create the DataBase with the required table
+ create and return the connection handler
+ insert data (list)


.. tabs::
   
   .. tab:: Code
    
    .. collapse:: Show Code

        .. literalinclude:: _static/codes/dbFunctions.py
                   :language: python
                   :linenos:
                   :emphasize-lines: 15, 31, 112, 121
      
      


|

|

Reading JSON Files
******************

----

If we have one subfolder with JSON sample files (e.g., :code:`mysamples\\weld_sample01.json`), it is desirable to read their content.

The main steps to read the JSON sample files:




.. tabs::
   
   .. tab:: (1)Create Files List
        
        Convert the subfolder (e.g., :code:`mysamples`) files into a Python List, which will be useful to iterate over them.
    
        List example: mySampleFiles = ['weld_sample01.json', 'weld_sample02.json', 'weld_sample03.json', ..., 'weld_samplexy.json']
    
        Code example:
        
        .. literalinclude:: _static/codes/fileslist.py
               :language: python
               :linenos:
               :emphasize-lines: 21
  
  
   .. tab:: (2)Create File Path
        
        Join the Current Working Directory, with the subfolder and with the JSON filename

        Example:
        
            :code:`filePath = C:\\Users\\Admin\\Dinasore\\mysamples\\weld_sample01.json`
            
            :code:`filePath = C:\\Users\\Admin\\Dinasore\\mysamples\\weld_sample02.json`
            
            ...
            
            :code:`filePath = C:\\Users\\Admin\\Dinasore\\mysamples\\weld_samplexy.json`
            
        

        Code Example:
        
        .. literalinclude:: _static/codes/filepath.py
               :language: python
               :linenos:
               
        Other methods also work.


   .. tab:: (3)Read JSON File

        Considering a List of JSON Files inside the "samples" subfolder:
        
        + Iterate over the JSON files
        + Create FilePath for the current file in the current iteration
        + Open the file
        + Load the JSON data (returns dictionary data type)
        + Extract the desired dictionary fields and append them to a dataList
        
        The conversion from dictionary to list is useful since it complies with the SQL Statement considered previously.
        
        Code Example:
        
        .. literalinclude:: _static/codes/readjson.py
               :language: python
               :linenos:
               :emphasize-lines: 1
        

        With the :code:`fileData` (dictionary Data Type) having the structure:
        
        .. literalinclude:: _static/codes/dictionary.py
               :language: python
               :linenos:
               
        
        .. warning::
            Do not forget to import the json library.
            
            
            
            


|

|

JSON to Database
****************

----


With the above ideas, the full example codes are:

.. tabs::
   
   .. tab:: (1) main.py
        
        Convert the subfolder (e.g., :code:`mysamples`) files into a Python List, which will be useful to iterate over them.
    
        List example: mySampleFiles = ['weld_sample01.json', 'weld_sample02.json', 'weld_sample03.json', ..., 'weld_samplexy.json']
    
        Code example:

        .. collapse:: Show Code

            .. literalinclude:: _static/codes/mainJson.py
                   :language: python
                   :linenos:
  
  
   .. tab:: (2) dbFunctions
        
        .. literalinclude:: _static/codes/dbFunctions.py
               :language: python
               :linenos:
               :emphasize-lines: 15, 28, 110, 119

  
  
   .. tab:: Results
   
        .. image:: _static/imgs/database.png
        
        
        
        
        
|

|

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



.. tabs::
   
   .. tab:: (1)Front Page
        
        .. admonition:: INFO
            
            This is the main grafana front page.
        
        .. image:: _static/imgs/pagina01.png
  
   .. tab:: (2)Access DataSources
        
        .. admonition:: INFO
            
            The Left tab allow us to access our Data Sources list, under the Configuration menu.
        
        .. image:: _static/imgs/pagina02.png
   
   .. tab:: (3)Adding New DataSource
        
        .. admonition:: INFO
        
            This page allow us to manage the added data sources and add new ones.
            
        .. image:: _static/imgs/pagina03.png
  
  
   .. tab:: (4)Search Available DataSources
        
        .. admonition:: INFO
        
            This search page allow us to choose the supported Data Sources by Grafana. For the current application, we will be using the **PostgreSQL**.
        
        .. image:: _static/imgs/pagina04.png

   
   .. tab:: (5)DataSource Settings
        
        .. admonition:: INFO
        
            The main settings to add/change:
            
            + Data Source Name
            + PostgreSQL Connection
                - host: :code:`db.fe.up.pt`
                - database name
                - username
                - password
                - TLS/SSL Mode **disabled**
            
            Then, after clicking the :code:`Save & Test` button, the data source is ready to be used (if the message "Database Connection OK" appears).
            
            
        
        .. image:: _static/imgs/pagina05.png
  
  
   .. tab:: (6)Checking DataSources List
        
        .. admonition:: INFO
        
            If the Data Source was successfully added it should be visible in the Data Sources List (under the configuration menu on the left tab)
        
        .. image:: _static/imgs/pagina06.png


|

The full steps are portrayed below:

.. image:: _static/imgs/addDataSource.gif













|


Exploring the Data Source
.........................


Before creating one dashboard, it could be useful to check if Grafana is being able to extract the data from our DataBase.



.. tabs::
   
   .. tab:: (1)Access to Explorer
        
        .. admonition:: INFO
            
            We explore the Data Source by clicking the **Explore** button.
        
        .. image:: _static/imgs/explore01.png
  
   .. tab:: (2)Testing Query
        
        .. admonition:: INFO
            
            To execute some query, follow the steps:
            
            + Select the desired output format (table, time series, etc);
            + Build the query with the Query Editor
            
        Example: query the database and display the column "time_start" values
        
        .. image:: _static/imgs/explore02.png
        
        |
        
        .. error:: 
        
            No data is retrieved. This usually happens due to the fact that Grafana usually sets automatically the highest search path. The workaround for this is to **Edit** the Query and add the schema.
            
            Example: the table **"WELD_SAMPLES"** would be replaced by **"DINASORE"."WELD_SAMPLES"** being "DINASORE" our schema.

        |
        
        By accessing the :code:`code` tab we can **edit** the Queries:
        
        .. image:: _static/imgs/explore03.png
        
        |
        
        And, after adding the schema it results:
        
        .. image:: _static/imgs/explore04.png
    

|


Creating Dashboard
..................


.. tabs::
   
   .. tab:: (1)Selecting DataSource
        
        .. admonition:: INFO
            
            The button "Build a Dashboard" quickly selects the desired data source to be used on the dashboard we want to create.
        

        .. image:: _static/imgs/d01.png
  
   .. tab:: (2)Adding Panel
        
        .. admonition:: INFO
            
            Dashboards may have a variety of elements. To start adding the first element, we can choose "Add a new Panel".
        
        .. image:: _static/imgs/d02.png
   
   .. tab:: (3)Building Queries
        
        .. admonition:: INFO
        
            This page allow us to configure our dashboard element. As for the data to be visualized, we build queries with the Query Editor which will provide the data.
            
        .. image:: _static/imgs/d03v2.png
  
  
   .. tab:: (4)Query Example
        
        .. admonition:: INFO
        
            For this example, the objective is to plot each row average force.
        
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
        
        .. literalinclude:: _static/codes/sqlavg.sql
            :language: sql
            :linenos:
        
        
        
        Since this code has more complexity, it is preferred to write it on the code Editor instead of using the Query Editor/Builder.
        
        |
        
        Limiting to just 50 welding samples:
        
        .. image:: _static/imgs/d04.png
        
        |
        
        With 5000 welding samples (change to :code:`LIMIT 5000`):

        .. image:: _static/imgs/d05.png



  
   .. tab:: (5)Saving the Dashboard
        
        .. admonition:: INFO
        
            After adding our queries and configuring our Dashboard we apply the changes to save it.
        
        |
        
        .. image:: _static/imgs/d06.png
        
        |
        
        Checking our panel:
        
        .. image:: _static/imgs/d07.png
        
        |
        
        Saving the Dashboard:
        
        .. image:: _static/imgs/d08.png
        
        

  
   .. tab:: (6)Multiple Queries
        
        .. admonition:: INFO
        
            It is also possible to have multiple queries on the same dashboard element.
        
        |
        
        .. image:: _static/imgs/d09.png
        
        |
        
        The queries used above are:
        
        .. literalinclude:: _static/codes/sqlavgqueries.sql
            :language: sql
            :linenos:
        
        
        
        
|

|