from core_queue import  PrintQueueManager 

cq =  PrintQueueManager()(capacity=3)

cq.enqueue_job("user1", "job101", 2)
cq.enqueue_job("user2", "job102", 3)
cq.show_status()

cq.dequeue_job()
cq.show_status()

cq.enqueue_job("user3", "job103", 1)
cq.enqueue_job("user4", "job104", 4)
cq.show_status()