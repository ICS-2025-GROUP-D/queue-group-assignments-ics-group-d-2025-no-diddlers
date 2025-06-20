from colorama import Fore, Back, Style, init
init()  # Initialize colorama for colored output

def show_status(self):
    #Displays the current state of the print queue in a user-friendly format
    print("\n=== PRINT QUEUE STATUS ===")
    if not self.queue:
        print("\n[STATUS] Print queue is empty")
        return
    
    print("\n=== CURRENT PRINT QUEUE STATUS ===")
    print(f"Total jobs in queue: {len(self.queue)}")
    print("\nJob Order (Next to print first):")
    print("-" * 60)
    print(f"{'Position':<10} | {'Job ID':<10} | {'User ID':<10} | {'Priority':<10} | {'Wait Time':<10}")
    print("-" * 60)
    
    for position, job in enumerate(self.queue, 1):
        print(f"{position:<10} | {job['job_id']:<10} | {job['user_id']:<10} | {job['priority']:<10} | {job['waiting_time']:<10}")
    
    print("-" * 60)
    print("=== END OF QUEUE STATUS ===\n")
    print("\nQueue Visualization:")
    print("[" + " | ".join(f"Job#{job['job_id']}(P{job['priority']})" for job in self.queue) + "]")
    
    # Print printer status
    if self.currently_printing:
        print(f"\n[PRINTER] Currently printing Job#{self.currently_printing['job_id']}")
    else:
        print("\n[PRINTER] Idle")

    for position, job in enumerate(self.queue, 1):
     # Color priority levels
        if job['priority'] == 1:
                priority_color = Fore.RED + str(job['priority']) + Style.RESET_ALL
        elif job['priority'] == 2:
                priority_color = Fore.YELLOW + str(job['priority']) + Style.RESET_ALL
        else:
                priority_color = Fore.GREEN + str(job['priority']) + Style.RESET_ALL
            
    print(f"{position:<10} | {job['job_id']:<10} | {job['user_id']:<10} | {priority_color:<10} | {job['waiting_time']:<10}")

#This is snapshot functionality to save the current queue state to a file
#This function can be called after any event that modifies the queue, such as enqueue or dequeue
def save_snapshot(self, event_type=""):

    #Saves the current queue state to a file with timestamp
    
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"queue_snapshot_{timestamp}_{event_type}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"Queue snapshot after event: {event_type}\n")
        f.write(f"Timestamp: {datetime.datetime.now()}\n\n")
        
        if not self.queue:
            f.write("Queue is empty\n")
        else:
            f.write("Current queue:\n")
            for job in self.queue:
                f.write(f"Job {job['job_id']} (User {job['user_id']}) - Priority {job['priority']} - Waiting {job['waiting_time']} ticks\n")
    
    print(f"[SNAPSHOT] Saved queue state to {filename}")
