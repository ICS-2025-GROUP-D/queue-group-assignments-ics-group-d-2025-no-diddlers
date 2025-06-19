"""
A priority-based job queue that implements priority aging.
Jobs are tuples: (priority, arrival_time, job_id, original_priority).
Lower priority number means higher priority.
"""

import time
from typing import Any, List, Tuple

class JobQueue:
    def __init__(self, aging_threshold_seconds: int = 10, aging_boost: int = 1):
        """
        args:
        aging_threshold_seconds (int): Time a job must wait before its
                                       priority is boosted.
        aging_boost (int): The amount to decrease the priority number by
                           (increasing its priority) during an aging event.
        """
        self.jobs: List[Tuple[int, float, Any, int]] = []
        self.aging_threshold = aging_threshold_seconds
        self.aging_boost = aging_boost

    def submit_job(self, job_id: Any, priority: int):
        """
        add a task/job to the queue

        Args:
            job_id: A unique identifier for the job.
            priority: The initial priority of the job.
        """
        arrival_time = time.time()
        job = (priority, arrival_time, job_id, priority)
        self.jobs.append(job)
        # Maintain the queue in sorted order (highest priority first)
        self.jobs.sort()

    def _perform_aging(self):
        """
        Checks all jobs in the queue and boosts the priority of any job
        that has been waiting longer than the aging threshold.
        """
        current_time = time.time()
        aged_jobs = False
        
        for i, (priority, arrival_time, job_id, original_priority) in enumerate(self.jobs):
            wait_time = current_time - arrival_time
            if wait_time > self.aging_threshold:
                new_priority = max(0, priority - self.aging_boost)
                if new_priority < priority:
                    self.jobs[i] = (new_priority, arrival_time, job_id, original_priority)
                    aged_jobs = True
        
        if aged_jobs:
            self.jobs.sort()

    def execute_next_job(self) -> Any:
        """
        Ages waiting jobs, then retrieves and executes the highest priority job.
        Tie-breaking is handled by arrival time automatically by the sort order.

        Returns:
            The job_id of the executed job, or None if the queue is empty.
        """
        if not self.jobs:
            return None

        self._perform_aging()

        # Pop the highest priority job (first element in the sorted list)
        _priority, _arrival_time, job_id, _original_priority = self.jobs.pop(0)
        return job_id

def main_simulation():
    """
    A simple simulation to demonstrate the JobQueue functionality.
    This runs silently and uses asserts to verify correctness.
    """
    print("--- Starting JobQueue Simulation ---")
    # Aging will occur for jobs waiting more than 2 seconds
    job_queue = JobQueue(aging_threshold_seconds=2, aging_boost=4)

    # Submit some initial jobs
    job_queue.submit_job("Data Processing", 10)
    job_queue.submit_job("API Request", 5)
    job_queue.submit_job("User Authentication", 2)
    
    # Execute the highest priority job immediately
    # Expected: "User Authentication" (priority 2)
    next_job = job_queue.execute_next_job()
    print(f"Executed: {next_job}")
    assert next_job == "User Authentication"

    # Wait long enough to trigger priority aging
    print("Waiting to trigger priority aging...")
    time.sleep(2.5)

    # Submit a new job with medium priority
    job_queue.submit_job("Image Upload", 6)

    # Now execute the next job.
    # "API Request" started at prio 5. After aging, it's prio 1.
    # "Data Processing" started at prio 10. After aging, it's prio 6.
    # "Image Upload" is prio 6.
    # Expected: "API Request" (prio 1)
    next_job = job_queue.execute_next_job()
    print(f"Executed: {next_job}")
    assert next_job == "API Request"

    # Execute next. Between "Data Processing" (prio 6) and "Image Upload" (prio 6),
    # "Data Processing" should win due to the tie-breaker (earlier arrival time).
    next_job = job_queue.execute_next_job()
    print(f"Executed: {next_job}")
    assert next_job == "Data Processing"

    # Execute the last job
    next_job = job_queue.execute_next_job()
    print(f"Executed: {next_job}")
    assert next_job == "Image Upload"
    
    # Try to execute from an empty queue
    next_job = job_queue.execute_next_job()
    print(f"Executed: {next_job}")
    assert next_job is None

    print("\n--- Simulation Complete: All assertions passed ---")

if __name__ == "__main__":
    main_simulation()