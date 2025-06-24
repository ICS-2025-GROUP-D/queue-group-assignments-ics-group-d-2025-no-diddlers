from JobSubmissionHandling import PrintQueueManager

def test_handle_simultaneous_submissions():
    pq = PrintQueueManager(capacity=6)
    jobs = [
        {'user_id': 'U1', 'job_id': 'J1', 'priority': 1},
        {'user_id': 'U2', 'job_id': 'J2', 'priority': 2},
        {'user_id': 'U3', 'job_id': 'J3', 'priority': 3}
    ]
    pq.handle_simultaneous_submissions(jobs)
    assert len(pq.queue) == 3
    assert any(job['job_id'] == 'J1' for job in pq.queue)
    assert any(job['job_id'] == 'J2' for job in pq.queue)
    assert any(job['job_id'] == 'J3' for job in pq.queue)