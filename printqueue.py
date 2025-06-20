import time

class PrintQueueManager:
    def __init__(self):
        self.jobs = []  # Each job: (priority, arrival_time, user_id, job_id, original_priority)
        self.aging_threshold_seconds = 10  # Time before aging applies
        self.aging_boost = 1               # Amount to boost priority
        self.expiry_seconds = 30           # Job expires after 30 seconds
        self.capacity = 10                 # Max jobs allowed in queue

    def enqueue_job(self, user_id, job_id, priority):
        """
        Adds a new job if there's room in the queue.
        """
        if len(self.jobs) >= self.capacity:
            print("Queue is full! Job rejected.")
            return

        arrival_time = time.time()
        job = (priority, arrival_time, user_id, job_id, priority)
        self.jobs.append(job)
        self.jobs.sort()  # Sort: lower number = higher priority

    def apply_priority_aging(self):
        """
        Boosts priority for jobs waiting longer than the aging threshold.
        """
        current_time = time.time()
        updated = False

        for i, (priority, arrival_time, user_id, job_id, original_priority) in enumerate(self.jobs):
            wait_time = current_time - arrival_time
            if wait_time >= self.aging_threshold_seconds:
                new_priority = max(0, priority - self.aging_boost)
                if new_priority < priority:
                    self.jobs[i] = (new_priority, arrival_time, user_id, job_id, original_priority)
                    updated = True

        if updated:
            self.jobs.sort()

    def remove_expired_jobs(self):
        """
        Removes jobs that have been waiting longer than expiry_seconds.
        """
        current_time = time.time()
        before = len(self.jobs)
        self.jobs = [
            job for job in self.jobs
            if current_time - job[1] <= self.expiry_seconds
        ]
        removed = before - len(self.jobs)
        if removed > 0:
            print(f"{removed} job(s) expired and removed from queue.")

    def tick(self):
        """
        Simulates time passing. Applies aging and removes expired jobs.
        """
        self.apply_priority_aging()
        self.remove_expired_jobs()

    def print_job(self):
        """
        Executes and removes the highest priority job from the queue.
        """
        if not self.jobs:
            print("No jobs to execute.")
            return None
        job = self.jobs.pop(0)
        print(f"Executed Job: {job[3]} from User: {job[2]}")
        return job[3]

    def show_status(self):
        """
        Prints a snapshot of the current queue state.
        """
        print("\n--- Current Queue ---")
        for priority, arrival_time, user_id, job_id, original_priority in self.jobs:
            wait_time = round(time.time() - arrival_time, 2)
            print(f"User: {user_id}, Job: {job_id}, Priority: {priority}, Wait Time: {wait_time}s")
        print("---------------------\n")

    def handle_simultaneous_submissions(self, job_list):
        """
        Accepts a list of jobs to submit at the same time.
        Format: [(user_id, job_id, priority), ...]
        """
        for user_id, job_id, priority in job_list:
            self.enqueue_job(user_id, job_id, priority)
