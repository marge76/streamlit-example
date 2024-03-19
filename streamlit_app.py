import streamlit as st
import boto3
from botocore.exceptions import ClientError

# Initialize the Lambda client
lambda_client = boto3.client('lambda')

# Define the name of your Lambda function
lambda_function_name = 'get-glue-datacatalog-column-names'

def call_lambda_function():
    try:
        # Call the Lambda function
        response = lambda_client.invoke(
            FunctionName=lambda_function_name,
            InvocationType='RequestResponse',
            Payload=b''
        )
        # Extract data from Lambda response
        data = response['Payload'].read().decode('utf-8')
        return data
    except ClientError as e:
        st.error(f"Error calling Lambda function: {e}")
        return None

def display_table(data):
    if data:
        try:
            # Parse JSON data
            rows = json.loads(data)
            # Display data in a table
            st.table(rows)
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON data: {e}")

def main():
    st.title('Display Table from Lambda Function')
    
    # Button to call Lambda function
    if st.button('Fetch Data'):
        # Call Lambda function and get data
        data = call_lambda_function()
        # Display data in a table
        display_table(data)

if __name__ == "__main__":
    main()
