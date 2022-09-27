import unittest
from checks.singledfchecks import SingleDataFrameChecks
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType

class TestSingleDfChecks(unittest.TestCase):

    employee_data = [("James", None,"Smith", 36636, "Male", 50000),
        ("Michael", None,"Rose", 40288, "Male", 60000),
        ("Robert", None,"Williams", 42114, "Male", 50000),
        ("Maria", "Anne","Jones", 39192, "Female", 70000),
        ("Jen", "Mary","Brown", 50389, "Female", 90000)]

    employee_schema = StructType([StructField("firstname", StringType(), nullable=False),
        StructField("middlename", StringType(), nullable=True),
        StructField("lastname", StringType(), nullable=False),
        StructField("employee_id", IntegerType(), nullable=False),
        StructField("gender", StringType(), nullable=False),
        StructField("salary", IntegerType(), nullable=False)])

    @classmethod
    def setUpClass(cls):
        cls.spark = (SparkSession.builder.appName("UnitTests").getOrCreate())

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()
        print("The spark session has been closed")


    def test_check_duplicates(self):
        employee = self.spark.createDataFrame(data=self.employee_data, schema=self.employee_schema)
        test_class = SingleDataFrameChecks(employee)
        self.assertEqual(test_class.check_duplicates(["employee_id"]), 'Passed')
        self.assertEqual(test_class.check_duplicates(["firstname", "employee_id"]), 'Passed')
        self.assertEqual(test_class.check_duplicates(["salary"]), 'Failed')
    
    def test_check_threshold_count(self):
        employee = self.spark.createDataFrame(data=self.employee_data, schema=self.employee_schema)
        test_class = SingleDataFrameChecks(employee)
        self.assertEqual(test_class.check_threshold_count(lower_limit=1, upper_limit=5), 'Passed')
        self.assertEqual(test_class.check_threshold_count(lower_limit=1, upper_limit=4), 'Failed')

    def test_check_empty(self):
        employee = self.spark.createDataFrame(data=self.employee_data, schema=self.employee_schema)
        test_class = SingleDataFrameChecks(employee)
        self.assertEqual(test_class.check_empty(), 'Passed')

if __name__ == '__main__':
    unittest.main()