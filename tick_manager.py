class PrintQueueManager:
    def __init__(self):
        self.queue = []
        self.aging_interval = 3 
        self.expiry_time = 10    
        self.tick_counter = 0

    def enqueue_job(self, user_id, job_id, priority):
        job = {
            'user_id': user_id,
            'job_id': job_id,
            'priority': priority,
            'waiting_time': 0,
            'arrival_tick': self.tick_counter
        }
        self.queue.append(job)
        self.sort_queue()

    def sort_queue(self):
        #Sorts by priority , if same , waiting time is considered (FIFO)
        self.queue.sort(key=lambda job: (-job['priority'], -job['waiting_time']))

    def tick(self):
        self.tick_counter += 1
        print(f"\n[Tick {self.tick_counter}] Advancing system time...")

        for job in self.queue:
            job['waiting_time'] += 1

        self.apply_priority_aging()
        self.remove_expired_jobs()
        self.sort_queue()

    def apply_priority_aging(self):
        for job in self.queue:
            if job['waiting_time'] > 0 and job['waiting_time'] % self.aging_interval == 0:
                job['priority'] += 1
                print(f"Aged Job {job['job_id']} (User {job['user_id']}) to priority {job['priority']}")

    def remove_expired_jobs(self):
        expired_jobs = [job for job in self.queue if job['waiting_time'] >= self.expiry_time]
        for job in expired_jobs:
            print(f"Job {job['job_id']} (User {job['user_id']}) expired after {job['waiting_time']} ticks.")
        self.queue = [job for job in self.queue if job['waiting_time'] < self.expiry_time]

    def show_status(self):
        print("\n--- Queue State ---")
        if not self.queue:
            print("Queue is empty.")
        else:
            for job in self.queue:
                print(f"User: {job['user_id']}, Job: {job['job_id']}, Priority: {job['priority']}, Waiting Time: {job['waiting_time']}")