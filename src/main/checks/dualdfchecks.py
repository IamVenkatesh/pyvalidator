from src.main.utils.logger import CustomLogger


class DualDataFrameChecks:
    """
        Summary: This class can be instantiated to perform checks available under this class to compare 2 different
        dataframes. The class expects the dataframes to be passed as a parameter during the instantiation.
        There is also an option to pass the log file location, but the default location would be the directory
        from which the class is instantiated. The default log file name is dualdfchecks.log.
        The default log level is 10: Debug.

        """

    def __init__(self, df1, df2, log_file_location='dualdfchecks.log'):
        self.df1 = df1
        self.df2 = df2
        self.logger_instance = CustomLogger(log_file_location, 10)
        self.logger = self.logger_instance.instantiate()

    def check_columns(self):
        """
        Summary: This function is used to check if all the columns present in the first dataframe is available
        in the second dataframe.

        Output: Returns the status of the test i.e. Passed or Failed

        """

        df1_columns = self.df1.columns
        df2_columns = self.df2.columns
        missing_columns = []

        for col in df1_columns:
            if col not in df2_columns:
                missing_columns.append(col)

        if len(missing_columns) > 0:
            self.logger.warning("The column present in df1 but not in df2 are: {0}".format(missing_columns))
            status = 'Failed'
        else:
            self.logger.info("The columns are same between the 2 dataframes")
            status = 'Passed'

        return status

    def check_datatype(self):
        """
        Summary: This function is used to check if all the columns & datatype of the first dataframe is the same as
        second dataframe.

        Output: Returns the status of the test i.e. Passed or Failed

        """

        df1_column_types = self.df1.dtypes
        df2_column_types = self.df2.dtypes
        difference = []

        for (col, dtype) in df1_column_types:
            if (col, dtype) not in df2_column_types:
                difference.append((col, dtype))

        if len(difference) > 0:
            self.logger.warning("The columns & datatype from df1 which are not in df2 are: {0}".format(difference))
            status = 'Failed'
        else:
            self.logger.info("The columns & datatypes are matching between df1 & df2")
            status = 'Passed'

        return status

    def check_distinct_values(self, col_df1, col_df2):
        """
        Summary: This function is used to check if the distinct values are the same between 2 different columns of a
        dataframes. For example, if the distinct values in Column A in Dataframe 1 is the same as the Column B in
        DataFrame 2.

        Output: Returns the status of the test i.e. Passed or Failed

        """

        df1_distinct_values = self.df1.select(col_df1).distinct().rdd.map(lambda x: x[0]).collect()
        df2_distinct_values = self.df2.select(col_df2).distinct().rdd.map(lambda x: x[0]).collect()
        common_values = set(df1_distinct_values).intersection(set(df2_distinct_values))

        missing_values_df1 = [value for value in df1_distinct_values if value not in common_values]
        missing_values_df2 = [value for value in df2_distinct_values if value not in common_values]

        if len(missing_values_df1) > 0 or len(missing_values_df2) > 0:
            status = 'Failed'
            self.logger.warning("The values present in df1 but missing in df2 are: {0}. "
                                "The values present in df2 but missing in df1 are: {1}".format(missing_values_df1,
                                                                                               missing_values_df2))
        else:
            self.logger.info("The values are matching between the 2 columns. The columns matched are: {0}, {1}".
                             format(col_df1, col_df2))
            status = 'Passed'

        return status

