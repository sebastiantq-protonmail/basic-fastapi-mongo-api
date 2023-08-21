from IncidenciasTipoBug.reportbug import BugReports

# Configurations import
from app.api.config.env import JIRA_USER, JIRA_PASSWORD, RABBITMQ_IP, RABBITMQ_QUEUE

# Configure RabbitMQ credentials at library initialization
bugReportsInstance = BugReports(user=JIRA_USER, password=JIRA_PASSWORD, host=RABBITMQ_IP, queue=RABBITMQ_QUEUE)