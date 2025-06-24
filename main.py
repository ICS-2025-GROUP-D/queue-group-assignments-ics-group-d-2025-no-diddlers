import time
from Priority_AgingSystem import PrintQueueManager

if __name__ == "__main__":
    pq = PrintQueueManager()

    pq.enqueue_job("user1", "job1", 10)
    pq.enqueue_job("user2", "job2", 5)
    pq.enqueue_job("user3", "job3", 2)

    pq.show_status()

    print("Executing one job (expect job3)...")
    pq.execute_next_job()

    print("Waiting to simulate aging...")
    time.sleep(11)  # Over the 10-second threshold

    pq.enqueue_job("user4", "job4", 6)

    print("Ticking (applying aging)...")
    pq.tick()

    pq.show_status()

    print("Executing next job (should be job2 due to aging)...")
    pq.execute_next_job()

    pq.show_status()