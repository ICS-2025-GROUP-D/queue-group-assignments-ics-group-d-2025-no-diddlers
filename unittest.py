#Reporting module test file
import unittest
import sys
import os
import time
from io import StringIO
from printqueue import PrintQueueManager
from visualization import PrintQueueVisualizer
from colorama import Fore

class TestEmptyQueueVisualization(unittest.TestCase):
    def setUp(self):
        self.manager = PrintQueueManager()
        self.visualizer = PrintQueueVisualizer(self.manager)
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def test_empty_queue_status(self):
        self.visualizer.show_status()
        output = self.held_output.getvalue()
        self.assertIn("Queue is empty", output)
        self.assertIn("STATUS", output)

    def tearDown(self):
        sys.stdout = sys.__stdout__

class TestBasicQueueVisualization(unittest.TestCase):
    def setUp(self):
        self.manager = PrintQueueManager()
        self.manager.enqueue_job(101, 1, 2)
        self.manager.enqueue_job(102, 2, 1)
        self.visualizer = PrintQueueVisualizer(self.manager)
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def test_basic_status_output(self):
        self.visualizer.show_status()
        output = self.held_output.getvalue()
        self.assertIn("101", output)
        self.assertIn("102", output)
        # Verify high priority job appears first
        self.assertTrue(output.find("102") < output.find("101"))

    def tearDown(self):
        sys.stdout = sys.__stdout__

class TestPriorityColoring(unittest.TestCase):
    def setUp(self):
        self.manager = PrintQueueManager()
        self.manager.enqueue_job(101, 1, 1)
        self.visualizer = PrintQueueVisualizer(self.manager)
    
    def test_priority_colors(self):
        color_str = self.visualizer._get_priority_color(1)
        self.assertIn(Fore.RED, color_str)
        color_str = self.visualizer._get_priority_color(3)
        self.assertIn(Fore.GREEN, color_str)

class TestSnapshotFunctionality(unittest.TestCase):
    def setUp(self):
        self.manager = PrintQueueManager()
        self.manager.enqueue_job(101, 1, 2)
        self.visualizer = PrintQueueVisualizer(self.manager)
        self.test_filename = "test_snapshot.txt"
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_snapshot_creation(self):
        self.visualizer.save_snapshot("test_event", filename=self.test_filename)
        self.assertTrue(os.path.exists(self.test_filename))
        with open(self.test_filename, 'r') as f:
            content = f.read()
            self.assertIn("Job 1", content)
            self.assertIn("test_event", content)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

class TestExpiredJobsVisualization(unittest.TestCase):
    def setUp(self):
        self.manager = PrintQueueManager()
        self.manager.enqueue_job(101, 1, 2)
        # Force expiry
        old_job = self.manager.jobs[0]
        expired_job = (old_job[0], time.time() - self.manager.expiry_seconds - 1,
                      old_job[2], old_job[3], old_job[4])
        self.manager.jobs[0] = expired_job
        self.visualizer = PrintQueueVisualizer(self.manager)
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def test_expiry_display(self):
        self.visualizer.show_status()
        output = self.held_output.getvalue()
        self.assertIn("EXPIRED", output)

    def tearDown(self):
        sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()
