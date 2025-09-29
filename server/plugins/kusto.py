from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table
from azure.identity import DefaultAzureCredential
import pandas as pd
import logging


class KustoQueryExecutor:
    """
    A class for executing Kusto queries against an Azure Data Explorer (ADX) cluster.
    Uses DefaultAzureCredential for authentication.
    """
    
    def __init__(self, cluster_url: str, database: str = None):
        """
        Initialize the Kusto Query Executor.
        
        Args:
            cluster_url (str): The ADX cluster URL (e.g., 'https://help.kusto.windows.net')
            database (str, optional): Default database name to use for queries
        """
        self.cluster_url = cluster_url
        self.database = database
        self.logger = logging.getLogger(__name__)
        
        # Initialize the connection string with DefaultAzureCredential
        self.kcsb = KustoConnectionStringBuilder.with_azure_token_credential(
            cluster_url, DefaultAzureCredential()
        )
        
        # Create the Kusto client
        self.client = KustoClient(self.kcsb)
        
    def execute_query(self, query: str, database: str = None) -> pd.DataFrame:
        """
        Execute a Kusto query and return results as a pandas DataFrame.
        
        Args:
            query (str): The Kusto query to execute
            database (str, optional): Database name (uses default if not specified)
            
        Returns:
            pd.DataFrame: Query results as a pandas DataFrame
            
        Raises:
            KustoServiceError: If the query execution fails
            ValueError: If no database is specified and no default is set
        """
        db_name = database or self.database
        if not db_name:
            raise ValueError("Database name must be specified either in constructor or method call")
            
        try:
            self.logger.info(f"Executing query against database: {db_name}")
            response = self.client.execute(db_name, query)
            
            # Convert to pandas DataFrame
            df = dataframe_from_result_table(response.primary_results[0])
            self.logger.info(f"Query executed successfully, returned {len(df)} rows")
            return df
            
        except KustoServiceError as e:
            self.logger.error(f"Kusto query failed: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during query execution: {e}")
            raise
    
    def execute_management_command(self, command: str, database: str = None) -> pd.DataFrame:
        """
        Execute a Kusto management command.
        
        Args:
            command (str): The management command to execute
            database (str, optional): Database name (uses default if not specified)
            
        Returns:
            pd.DataFrame: Command results as a pandas DataFrame
        """
        db_name = database or self.database
        if not db_name:
            raise ValueError("Database name must be specified either in constructor or method call")
            
        try:
            self.logger.info(f"Executing management command against database: {db_name}")
            response = self.client.execute_mgmt(db_name, command)
            
            # Convert to pandas DataFrame
            df = dataframe_from_result_table(response.primary_results[0])
            self.logger.info(f"Management command executed successfully")
            return df
            
        except KustoServiceError as e:
            self.logger.error(f"Kusto management command failed: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during management command execution: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test the connection to the ADX cluster.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            # Simple query to test connection
            test_query = "print 'Connection test successful'"
            db_name = self.database or "Hub"  # Use a default system database for testing
            
            response = self.client.execute(db_name, test_query)
            self.logger.info("Connection test successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
    
    def get_databases(self) -> pd.DataFrame:
        """
        Get list of databases available on the cluster.
        
        Returns:
            pd.DataFrame: List of databases
        """
        try:
            command = ".show databases"
            # Use any database for management commands, or a system database
            db_name = self.database or "Hub"
            return self.execute_management_command(command, db_name)
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve databases: {e}")
            raise
    
    def get_tables(self, database: str = None) -> pd.DataFrame:
        """
        Get list of tables in the specified database.
        
        Args:
            database (str, optional): Database name (uses default if not specified)
            
        Returns:
            pd.DataFrame: List of tables
        """
        command = ".show tables"
        return self.execute_management_command(command, database)
    
    def close(self):
        """
        Close the Kusto client connection.
        """
        if hasattr(self.client, 'close'):
            self.client.close()
            self.logger.info("Kusto client connection closed")