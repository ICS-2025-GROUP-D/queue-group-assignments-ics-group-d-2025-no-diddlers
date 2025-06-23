# Configuration file for the print queue system
# Number of ticks after which a job is considered expired
EXPIRY_TICKS = 300  # Example: 300 ticks = 5 minutes if a tick is 1 second

# Maximum number of jobs the queue can hold
QUEUE_CAPACITY = 100  # Adjust based on system limits

# Log file path or logging configuration (if needed)
LOG_FILE = 'logs/print_queue.log'

# Priority levels (optional, for easier reference)
PRIORITY_LEVELS = {
    1: 'High',
    2: 'Medium',
    3: 'Low'
}

# Server configuration (optional)
HOST = '127.0.0.1'
PORT = 5000
DEBUG = True
