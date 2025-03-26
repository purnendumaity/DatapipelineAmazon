# DatapipelineAmazon
=============This repository has below folder structure===========
After downloading given file we have saved in subfolder /input_file
Pyspark has hadoop dependency so that is inside subfolder hadoop-3.3.6
Also Pyspark has JVM dependency which we have indicated in the program
by attaching that path to environment variable
During Pyspark processing partition file gets saved inside subfolder processed_data
Final output file gets saved inside subfolder output_file
For Remote TiDB Cloud connection security certificate needed, that is 
inside subfolder ssl_certificate
DatapipelineAmazon
--subdirectory--/processed_data
--subdirectory--/output_file
--subdirectory--/input_file
--subdirectory--/hadoop-3.3.6
--subdirectory--/ssl_certificate
Pysparkcsvprocessing.py
remotedbinsertcsv.py
All SQL commands.txt
Readme.txt

=========Additional Notes related to Hadoop Dependency=============
Pyspark needs Hadoop but it works easily in Unix but not in Windows machine.
1st we have to download the Hadoop windows utility from below url
https://github.com/cdarlint/winutils,
Then we extract zip file and utilize hadoop-3.3.6 folder
After that to give requisite permission to Hadoop winutils we have to use below command
in Command prompt through admin user.
My project path is:D:\Python-Projects\DatapipelineAmazon
D:\Python-Projects\DatapipelineAmazon\hadoop-3.3.6\bin>winutils.exe chmod 777 D:/Python-Projects/DatapipelineAmazon


=========This repository has 2 Python file and "All SQL commands.txt"=============
I have not purposefully linked both the python program because better to do individual testing.

---1st run the Pysparkcsvprocessing.py----
It utilizes Pyspark package to do all cleaning and transformation steps.
During Pyspark processing partition file gets saved in processed_data
Then we join all parttion chunks and create Final output file which gets saved in output_file.
During processing initially it shows input file schema, 1st 5 rows, file total line count.
We are doing deduplication based on review_id column, it prints the duplicate review_id
values in console, then it shows post-deduplication line counts.
Then it does all further processing as required.

---2nd run the remotedbinsertcsv.py----
Through this the cleaned output file data gets loaded into remote TiDB Cloud database.
We have to create a TiDB Cloud database account first and create a test database.
We have to also check whether our computer IP address is added in their allow list/firewall rule.
We need to download the security certificate as per their instruction and save in local machine.
We create a dictionary mapping of MySQL datatypes and Pandas datatypes
That we utilize to programmatically create a Create Table statement
and then do Insert via batches with parameterized SQL.

---3rd we can check/test All SQL commands.txt----
This file has various SQL statements which I have prepared 
to analyze the data as per requirement.
 
