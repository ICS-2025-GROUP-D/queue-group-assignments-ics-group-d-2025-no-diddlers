from colorama import Fore, Back, Style, init
import time
from datetime import datetime
init()

class PrintQueueVisualizer:
    def __init__(self, queue_manager):
        self.queue_manager = queue_manager  # Accept either PrintQueueManager implementation

    def _get_priority_color(self, priority):
        """Returns colored priority string based on priority level"""
        if priority <= 1:  # Highest priority
            return Fore.RED + f"{priority} (Urgent)" + Style.RESET_ALL
        elif priority <= 3:
            return Fore.YELLOW + str(priority) + Style.RESET_ALL
        else:
            return Fore.GREEN + str(priority) + Style.RESET_ALL

    def _get_wait_time(self, job):
        """Handles both time-based and tick-based systems"""
        if hasattr(self.queue_manager, 'tick_counter'):  # Tick-based system
            return f"{job.get('waiting_time', 0)} ticks"
        else:  # Time-based system
            return f"{time.time() - job[1]:.1f}s" if isinstance(job, tuple) else "N/A"

    def show_status(self):
        """Universal status display for both queue implementations"""
        print("\n" + "="*60)
        print("=== PRINT QUEUE STATUS ===".center(60))
        print("="*60)

        # Handle empty queue
        if not self.queue_manager.jobs and not self.queue_manager.queue:
            print("\n[STATUS] Queue is empty")
            return

        # Determine current jobs based on implementation
        if hasattr(self.queue_manager, 'jobs'):  # printqueue.py implementation
            jobs = self.queue_manager.jobs
            current_printing = None  # This implementation doesn't track currently printing job
        else:  # tick_manager.py implementation
            jobs = self.queue_manager.queue
            current_printing = None  # Add tracking if needed

        # Print queue summary
        print(f"\nTotal Jobs: {len(jobs)}")
        if hasattr(self.queue_manager, 'capacity'):
            print(f"Queue Capacity: {len(jobs)}/{self.queue_manager.capacity}")
        
        # Print job table
        print("\nJob Order (Next to print first):")
        print("-" * 100)
        print(f"{'Position':<8} | {'Job ID':<8} | {'User ID':<8} | {'Priority':<15} | {'Wait Time':<12} | {'Status':<10}")
        print("-" * 100)

        for pos, job in enumerate(jobs, 1):
            # Extract job details based on implementation
            if isinstance(job, tuple):  # printqueue.py
                priority, _, user_id, job_id, orig_priority = job
                wait_time = time.time() - job[1]
                is_expired = wait_time > self.queue_manager.expiry_seconds
            else:  # tick_manager.py
                priority = job['priority']
                user_id = job['user_id']
                job_id = job['job_id']
                wait_time = job['waiting_time']
                is_expired = wait_time >= self.queue_manager.expiry_time

            status = Fore.RED + "EXPIRED" + Style.RESET_ALL if is_expired else "Active"
            
            print(
                f"{pos:<8} | {job_id:<8} | {user_id:<8} | "
                f"{self._get_priority_color(priority):<15} | "
                f"{self._get_wait_time(job):<12} | "
                f"{status:<10}"
            )

        print("-" * 100)

        # Print printer status
        printing_status = "Idle"
        if current_printing:
            printing_status = f"Printing Job {current_printing}"
        print(f"\n[PRINTER STATUS] {printing_status}")

        # Print ASCII visualization
        print("\nQueue Visualization:")
        print("[" + " | ".join(
            f"#{job[3] if isinstance(job, tuple) else job['job_id']}"
            f"(P{job[0] if isinstance(job, tuple) else job['priority']})"
            f"{'!' if is_expired else ''}"
            for job in jobs
        ) + "]")

    def save_snapshot(self, event_type=""):
        """Universal snapshot for both implementations"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"queue_snapshot_{timestamp}_{event_type}.txt"
        
        with open(filename, 'w') as f:
            f.write(f"=== Queue Snapshot ===\n")
            f.write(f"Event: {event_type}\n")
            f.write(f"Timestamp: {datetime.now()}\n")
            
            if hasattr(self.queue_manager, 'jobs'):  # printqueue.py
                jobs = self.queue_manager.jobs
                f.write(f"System: Time-based (seconds)\n")
                f.write(f"Expiry: {self.queue_manager.expiry_seconds}s\n")
            else:  # tick_manager.py
                jobs = self.queue_manager.queue
                f.write(f"System: Tick-based\n")
                f.write(f"Current Tick: {self.queue_manager.tick_counter}\n")
                f.write(f"Expiry: {self.queue_manager.expiry_time} ticks\n")
            
            f.write(f"\nJobs ({len(jobs)}):\n")
            for job in jobs:
                if isinstance(job, tuple):  # printqueue.py
                    f.write(
                        f"Job {job[3]} (User {job[2]}) | "
                        f"Priority: {job[0]} | "
                        f"Waiting: {time.time() - job[1]:.1f}s\n"
                    )
                else:  # tick_manager.py
                    f.write(
                        f"Job {job['job_id']} (User {job['user_id']}) | "
                        f"Priority: {job['priority']} | "
                        f"Waiting: {job['waiting_time']} ticks\n"
                    )
        
        print(f"[SNAPSHOT] Saved to {filename}")

# Example usage:
if __name__ == "__main__":
    # Test with either implementation
    from tick_manager import PrintQueueManager as TickManager
    # from printqueue import PrintQueueManager as TimeManager
    
    manager = TickManager()
    manager.enqueue_job(101, 1, 3)
    manager.enqueue_job(102, 2, 1)
    
    visualizer = PrintQueueVisualizer(manager)
    visualizer.show_status()
    
    # Simulate some ticks
    for _ in range(5):
        manager.tick()
    
    visualizer.show_status()
    visualizer.save_snapshot("test_run")
