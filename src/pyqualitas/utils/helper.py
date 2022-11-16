from pyspark.sql import SparkSession, udf
from pyspark.sql.types import StringType
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import datetime
import os


class Helper:

    def __init__(self, spark: SparkSession):
        self.spark = spark

    def create_hive_table_df(self, database_name, table_name):
        """
        Summary: This function is a helper to read the hive database table to spark dataframe

        Parameters: Database Name & Table Name

        Output: Returns a spark dataframe
        """
        return self.spark.table("{0}.{1}".format(database_name, table_name))

    def create_hdfs_files_df(self, format_type, hdfs_location, infer_schema=True):
        """
        Summary: This function is a helper to read the hdfs files to spark dataframe

        Parameters: HDFS File Format, HDFS File Location, True or False for inferSchema. By Default the values is
        set to true.

        Output: Returns a spark dataframe
        """
        return self.spark.read.format(format_type).option("header", True) \
            .option("inferSchema", infer_schema).load(hdfs_location)

    def create_dataframe(self, dataframe, schema):
        """
        Summary: This function is a helper to create a spark dataframe

        Parameters: Data on which the dataframe has to be created, schema of the data

        Output: Returns a spark dataframe
        """
        return self.spark.createDataFrame(data=dataframe, schema=schema)

    @staticmethod
    def publish_udf(function, return_type=StringType()):
        """
        Summary: This function is a helper to generate udf from a python function

        Parameters: Python function with parameters, Return Type of the function i.e. StringType, FloatType, DateType etc

        Output: Publishes an udf based on the python function        
        """
        return udf(lambda *args: function, return_type)


    @staticmethod
    def generate_report_csv(test_results, file_location):
        """
        Summary: This static function is a helper to save the test results in a csv file
        
        Parameters: The output from the checksuite method, location where the csv file has to be saved. For example: /home/pyqualitas/TestResults.csv
        
        Output: A csv file written to the user defined location
        """
        results = pd.DataFrame(data=test_results, columns=["TestName", "TestDescription", "Status"])
        return results.to_csv(file_location, index=False)

    @staticmethod
    def generate_html_report(test_results, file_location):
        """
        Summary: This static function is a helper to save the test results in a html file
        
        Parameters: The output from the checksuite method, location where the HTML file has to be saved. For example: /home/pyqualitas/TestResults.html
        
        Output: A html file written to the user defined location
        """
        test_result_df = pd.DataFrame(data=test_results, columns=["TestName", "TestDescription", "Status"])
        results_table = test_result_df.to_html(index=False)
        total_test_count = len(test_result_df)
        total_pass_count = len(test_result_df[test_result_df['Status'] == 'Passed'])
        total_fail_count = len(test_result_df[test_result_df['Status'] == 'Failed'])
        template_file_location = os.path.join(os.path.dirname(__file__), 'template')
        env = Environment(loader=FileSystemLoader(template_file_location))
        template = env.get_template('TestResult.html')
        html = template.render(results_table=results_table, total_test_count=total_test_count,
                               total_pass_count=total_pass_count, total_fail_count=total_fail_count,
                               report_time=datetime.datetime.now())
        with open(file_location, "w") as file:
            file.write(html)
        file.close()
