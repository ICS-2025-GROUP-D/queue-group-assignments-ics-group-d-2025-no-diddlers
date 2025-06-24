from print_queue_manager import  PrintQueueManager 

pq =  PrintQueueManager()(capacity=3)

pq.enqueue_job("user1", "job101", 2)
pq.enqueue_job("user2", "job102", 3)
pq.show_status()

pq.dequeue_job()
pq.show_status()

pq.enqueue_job("user3", "job103", 1)
pq.enqueue_job("user4", "job104", 4)
pq.show_status()
