import time

class PrintQueueManager:
    def __init__(self):
        # Each job: (priority, arrival_time, user_id, job_id, original_priority)
        self.jobs = []
        self.aging_threshold_seconds = 10  # After 10s, job gains higher priority
        self.aging_boost = 1               # Priority improves by this amount

    def enqueue_job(self, user_id, job_id, priority):
        """
        Adds a job to the queue with initial priority and metadata.
        """
        arrival_time = time.time()
        job = (priority, arrival_time, user_id, job_id, priority)
        self.jobs.append(job)
        self.jobs.sort()  # Sort: lower number = higher priority

    def apply_priority_aging(self):
        """
        Boosts priority for jobs waiting longer than the aging threshold.
        """
        current_time = time.time()
        aged = False

        for i, (priority, arrival_time, user_id, job_id, original_priority) in enumerate(self.jobs):
            wait_time = current_time - arrival_time
            if wait_time > self.aging_threshold_seconds:
                new_priority = max(0, priority - self.aging_boost)
                if new_priority < priority:
                    self.jobs[i] = (new_priority, arrival_time, user_id, job_id, original_priority)
                    aged = True

        if aged:
            self.jobs.sort()  # Re-sort after any priority change

    def tick(self):
        """
        Simulate time passing — applies aging logic.
        """
        self.apply_priority_aging()

    def execute_next_job(self):
        """
        Executes and removes the job with the highest priority.
        """
        if not self.jobs:
            print("No jobs to execute.")
            return None
        job = self.jobs.pop(0)
        print(f"Executed Job: {job[3]} from User: {job[2]}")
        return job[3]

    def show_status(self):
        """
        Displays current queue snapshot.
        """
        print("\n--- Current Queue ---")
        for priority, arrival_time, user_id, job_id, original_priority in self.jobs:
            wait_time = round(time.time() - arrival_time, 2)
            print(f"User: {user_id}, Job: {job_id}, Priority: {priority}, Wait Time: {wait_time}s")
        print("---------------------\n")

