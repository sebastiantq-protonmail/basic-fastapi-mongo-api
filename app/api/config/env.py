import os

# Add here all the environment variables

# Basic configuration
API_NAME = os.getenv('API_NAME')
JWT_SECRET = os.getenv('JWT_SECRET') # The JWT secret string
MONGO_CLIENT = os.getenv('MONGO_CLIENT') # Something like: mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]

# IncidentsBug library configuration
JIRA_PROJECT_ID = os.getenv('JIRA_PROJECT_ID')
JIRA_USER = os.getenv('JIRA_USER') # Your Jira credentials
JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')
RABBITMQ_IP = os.getenv('RABBITMQ_IP') # Ask someone for the assigned server for this project
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')