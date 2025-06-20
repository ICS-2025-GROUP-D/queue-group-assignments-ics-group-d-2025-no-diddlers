from flask import Flask, render_template
from queue import Queue
from datetime import datetime
import config # Assuming config.py contains necessary configurations
from flask import request
app = Flask(__name__)

@app.route('/')
def dashboard():
    pq = Queue()  
   
    return render_template('index.html',
    queue=pq.queue,
    current_job=pq.currently_printing_job,
    last_update=datetime.now(),
    capacity=pq.queue_capacity,
    expiry_threshold=config.EXPIRY_TICKS,
    high_priority_count=len([j for j in pq if j.priority == 1]),
    medium_priority_count=len([j for j in pq if j.priority == 2]),
    low_priority_count=len([j for j in pq if j.priority == 3]),
    queue_version="1.0.0"
)
    
if __name__ == '__main__':
    app.run(debug=True)
