import threading
class PrintQueueManager:
    def __init__(self, capacity=11):
        self.queue = []
        self.capacity = capacity
        self.lock = threading.Lock()

    def enqueue_job(self, user_id, job_id, priority):
        with self.lock:
            if len(self.queue) < self.capacity:
                job = {
                    'user_id': user_id,
                    'job_id': job_id,
                    'priority': priority,
                    'waiting_time': 0
                }
                self.queue.append(job)
                print(f"Job {job_id} submitted by User {user_id}.")
            else:
                print("Queue is full. Job cannot be submitted.")

    def handle_simultaneous_submissions(self, jobs):
        threads = []
        for job in jobs:
            user_id, job_id, priority = job
            thread = threading.Thread(target=self.enqueue_job, args=(user_id, job_id, priority))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()




