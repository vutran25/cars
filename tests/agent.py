"""
Unit tests for agent module.
"""
import unittest
import datetime
from dealer.agent import Agent

TEST_AGENTS = [{"agent_id": "1", "expertise": [0, 1, 2, 3],
                "service_time": 3, "rating": 0.111},
               {"agent_id": "2", "expertise": [3, 1, 2, 0],
                "service_time": 4, "rating": 0.222}]
TEST_CUSTOMERS = [{"arrival_time": datetime.datetime(2018, 7, 15, 8, 0, 0, 0),
                   "interest": 1,
                   "sale_closed": True},
                  {"arrival_time": datetime.datetime(2018, 7, 15, 9, 0, 0, 0),
                   "interest": 0,
                   "sale_closed": False},
                  {"arrival_time": datetime.datetime(2018, 7, 15, 11, 0, 0, 0),
                   "interest": 2,
                   "sale_closed": True}]


class TestAgent(unittest.TestCase):
    """
    Tests for agent.
    """

    def setUp(self):
        for agent in TEST_AGENTS:
            Agent.innit(agent)

    def test_2_agents_done_at_once(self):
        """
        Test for picking the highest rating agent
        and picking the right agent when two agents are finish at the same time
        """
        # Test highest rating agent
        agent, wait_time = Agent.get(TEST_CUSTOMERS[0])
        self.assertEqual(
            (TEST_AGENTS[1], 0), (agent.agent, wait_time))
        # Test 2 agents done at the same time
        Agent.get(TEST_CUSTOMERS[1])
        agent, wait_time = Agent.get(TEST_CUSTOMERS[2])
        self.assertEqual(
            (TEST_AGENTS[1], 60), (agent.agent, wait_time))


if __name__ == "__main__":
    unittest.main()
