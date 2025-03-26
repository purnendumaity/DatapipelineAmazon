import pandas as pd
import pymysql
import os
import time

# Start Timer
start_time = time.time()

#TiDB Connection Details
conn = pymysql.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    port=4000,user="y4NrAMiYRskbnuc.root",password="CaQyJFFav4bz3zVF",database="test",
    ssl_verify_cert=True,ssl_verify_identity=True,
    ssl_ca="./ssl_certificate/isrgrootx1.pem"
)
cursor = conn.cursor()

#Final Processed CSV File Path
csv_file_path = "./output_file/final_cleaned_awsdata.csv"
batch_size = 1000  # Define batch size for inserts

#Infer Schema from CSV
#Read sample to infer schema
df = pd.read_csv(csv_file_path, nrows=10)
#Map Pandas dtypes to MySQL Data Types
pandas_to_mysql = {
    "int64": "BIGINT",
    "float64": "DOUBLE",
    "bool": "BOOLEAN",
    "object": "VARCHAR(500)",  # Strings are treated as VARCHAR
    "datetime64[ns]": "DATETIME"
}

#some longtext column issue so here forcing them
long_text_columns = {"review_body", "review_headline", "product_title"}

#Generate CREATE TABLE Statement
create_table_sql = "CREATE TABLE aws_reviews (\n"
for col in df.columns:
    pandas_dtype = str(df[col].dtype)
    # Default to TEXT if unknown and handling longtext
    mysql_type = "TEXT" if col in long_text_columns else pandas_to_mysql.get(pandas_dtype, "TEXT")
    #mysql_type = pandas_to_mysql.get(pandas_dtype, "TEXT")
    create_table_sql += f"    {col} {mysql_type},\n"
create_table_sql = create_table_sql.rstrip(",\n") + "\n);"

print("Generated SQL Table Schema:\n", create_table_sql)

# Execute Table Creation in TiDB
try:
    cursor.execute("DROP TABLE IF EXISTS aws_reviews;")  # Drop if exists
    cursor.execute(create_table_sql)  # Create table
    conn.commit()
    print("Table aws_reviews created successfully!")
except Exception as e:
    print("Error Creating Table:", e)

#Insert Data in Batches
print("Starting Data Insertion...")

# Read CSV in chunks
for chunk in pd.read_csv(csv_file_path, chunksize=batch_size):
    # Convert DataFrame to List of Tuples
    data_tuples = chunk.to_records(index=False).tolist()
    #Dynamically create INSERT statement
    columns = ", ".join(chunk.columns)
    values_placeholder = ", ".join(["%s"] * len(chunk.columns))
    insert_sql = f"INSERT INTO aws_reviews ({columns}) VALUES ({values_placeholder})"
    #Batch Insert into TiDB
    cursor.executemany(insert_sql, data_tuples)
    conn.commit()
    print(f"Inserted {len(data_tuples)} rows...")

#Close Database Connection**
cursor.close()
conn.close()

print("Data Insertion Completed Successfully!")

end_time = time.time()
total_seconds = end_time - start_time
formatted_time = time.strftime("%H:%M:%S", time.gmtime(total_seconds))
print(f" Total Execution Time: {formatted_time}")
