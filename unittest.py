import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from  printqueue import PrintQueueManager
from io import StringIO

#Test case for PrintQueueManager to check empty queue visualization
class TestEmptyQueueVisualization(unittest.TestCase):
    def setUp(self):
        self.pq = PrintQueueManager(capacity=5)
        # Redirect stdout to capture print output
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def test_empty_queue_status(self):
        self.pq.show_status()
        output = self.held_output.getvalue()
        self.assertIn("Queue is empty", output)
        self.assertIn("STATUS", output)

    def tearDown(self):
        sys.stdout = sys.__stdout__
 
#Test case for PrintQueueManager to check basic queue visualization
class TestBasicQueueVisualization(unittest.TestCase):
    def setUp(self):
        self.pq = PrintQueueManager(capacity=5)
        self.pq.enqueue_job(101, 1, 2)
        self.pq.enqueue_job(102, 2, 1)
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def test_basic_status_output(self):
        self.pq.show_status()
        output = self.held_output.getvalue()
        
        # Test table headers
        self.assertIn("Position", output)
        self.assertIn("Job ID", output)
        self.assertIn("Priority", output)
        
        # Test job data
        self.assertIn("101", output)
        self.assertIn("102", output)
        
        # Test ordering (priority 1 should come first)
        self.assertTrue(output.find("102") < output.find("101"))

    def tearDown(self):
        sys.stdout = sys.__stdout__
    
#Test case for PrintQueueManager to check queue status with color output
class TestPriorityColoring(unittest.TestCase):
    def setUp(self):
        self.pq = PrintQueueManager(capacity=5)
        self.pq.enqueue_job(101, 1, 1)  # High priority
        self.pq.enqueue_job(102, 2, 3)  # Low priority
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def test_priority_colors(self):
        # Only run if colorama is being used
        if 'colorama' in sys.modules:
            from colorama import Fore
            self.pq.show_status()
            output = self.held_output.getvalue()
            
            # Test color codes appear in output
            self.assertIn(Fore.RED, output)  # High priority
            self.assertIn(Fore.GREEN, output)  # Low priority

    def tearDown(self):
        sys.stdout = sys.__stdout__

#Test case for PrintQueueManager to check snapshot functionality
import datetime
class TestSnapshotFunctionality(unittest.TestCase):
    def setUp(self):
        self.pq = PrintQueueManager(capacity=5)
        self.pq.enqueue_job(101, 1, 2)
        self.test_filename = "test_snapshot.txt"
        
        # Cleanup any existing test file
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_snapshot_creation(self):
        self.pq.save_snapshot("test_event", filename=self.test_filename)
        
        # Verify file was created
        self.assertTrue(os.path.exists(self.test_filename))
        
        # Verify content
        with open(self.test_filename, 'r') as f:
            content = f.read()
            self.assertIn("Job 1", content)
            self.assertIn("test_event", content)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

#Test case for PrintQueueManager to check empty queue snapshot functionality
import os
class TestEmptyQueueSnapshot(unittest.TestCase):
    def setUp(self):
        self.pq = PrintQueueManager(capacity=5)
        self.test_filename = "empty_snapshot.txt"
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_empty_snapshot(self):
        self.pq.save_snapshot("empty_test", filename=self.test_filename)
        
        with open(self.test_filename, 'r') as f:
            content = f.read()
            self.assertIn("Queue is empty", content)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

#Test case for PrintQueueManager to check aging effect on job priority
import unittest
class TestAgingVisualization(unittest.TestCase):
    def setUp(self):
        self.pq = PrintQueueManager(capacity=5)
        self.pq.enqueue_job(101, 1, 3)  # Low priority
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def test_aging_effect_display(self):
        # Force aging by setting high waiting time
        self.pq.queue[0]['waiting_time'] = 10
        self.pq.apply_priority_aging()
        
        self.pq.show_status()
        output = self.held_output.getvalue()
        
        # Verify priority changed from 3 to 2
        self.assertIn("Priority: 2", output)

    def tearDown(self):
        sys.stdout = sys.__stdout__

#Test case for PrintQueueManager to check expired jobs visualization
import unittest
class TestExpiredJobsVisualization(unittest.TestCase):
    def setUp(self):
        self.pq = PrintQueueManager(capacity=5, max_wait_time=5)
        self.pq.enqueue_job(101, 1, 2)
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def test_expiry_notification(self):
        # Force expiry
        self.pq.queue[0]['waiting_time'] = 10
        expired_count = self.pq.check_and_notify_expiry()
        
        output = self.held_output.getvalue()
        self.assertEqual(expired_count, 1)
        self.assertIn("expired", output)

    def tearDown(self):
        sys.stdout = sys.__stdout__

# Test suite to run all test cases
import unittest
def create_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestEmptyQueueVisualization))
    suite.addTest(unittest.makeSuite(TestBasicQueueVisualization))
    suite.addTest(unittest.makeSuite(TestPriorityColoring))
    suite.addTest(unittest.makeSuite(TestSnapshotFunctionality))
    suite.addTest(unittest.makeSuite(TestEmptyQueueSnapshot))
    suite.addTest(unittest.makeSuite(TestAgingVisualization))
    suite.addTest(unittest.makeSuite(TestExpiredJobsVisualization))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = create_test_suite()
    runner.run(test_suite)
