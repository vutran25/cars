"""
Agent object.
"""

import datetime
from data import CARS


class Agent(object):
    """
    Car sales agent.
    """
    working_agents, agents_info = [], []
    week_start = 0

    def __init__(self, agent, customer):
        self.deals_closed = []
        self.time_available = customer["arrival_time"]
        self.commission = 0
        self.agent = agent

    @classmethod
    def innit(cls, agent):
        """
        Initialize agents info
        """
        cls.agents_info.append(agent)

    @classmethod
    def get(cls, customer):
        """
        Assign the best agent for the customer, creating an instance if necessary.
        Return the agent and wait time (0 if an agent is readily available).
            - customer: Info of customer.
        """
        # Create 5 instance of agents if not created yet
        if not cls.working_agents:
            cls.week_start = customer["arrival_time"]
            for agent in cls.agents_info:
                cls.working_agents.append(cls(agent, customer))
        # If there are already 5 instance agents created
        available_agents = list(
            filter(lambda a: a.time_available <= customer["arrival_time"], cls.working_agents))
        # If there are available agents
        if available_agents:
            agent = pick_agent(available_agents, customer)
            agent.add_customer(customer)
            return (agent, 0)
        # If all agents are busy with customers
        # Sort by the time agents will be available and pick the earlest to be ready
        else:
            cls.working_agents.sort(key=lambda a: a.time_available)
            if cls.working_agents[0].time_available == cls.working_agents[1].time_available:
                done_first_agents = list(
                    filter(lambda a: a.time_available == cls.working_agents[0].time_available,
                           cls.working_agents))
                agent = pick_agent(done_first_agents, customer)
                agent.add_customer(customer)
                return (agent, (agent.time_available - datetime.timedelta(
                    hours=agent.agent["service_time"]) - customer["arrival_time"]).seconds//60)
            else:
                cls.working_agents[0].add_customer(customer)
                return (cls.working_agents[0],
                        (cls.working_agents[0].time_available - datetime.timedelta(
                            hours=cls.working_agents[0].agent["service_time"]) -
                         customer["arrival_time"]).seconds//60)

    def add_customer(self, customer):
        """
        When an agent is getting a new customer,
        that customer will affect some performace of that agent
            -time_available will increase
            -deals_closed will have more deal or not
        """
        if self.time_available <= customer["arrival_time"]:
            self.time_available = customer["arrival_time"]
        self.time_available += datetime.timedelta(
            hours=self.agent["service_time"])
        if customer["sale_closed"]:
            self.deals_closed.append((customer))

    def performace_report(self):
        """
        Generate Report
        Return: (ID, # of deals, revenue, commission, bonus)
        """
        revenue, bonus = 0, 0
        for deal in self.deals_closed:
            revenue += CARS[deal["interest"]]["price"]
        week = 0
        if len(self.deals_closed) >= 10:
            weeks = (self.deals_closed[-1]
                     ["arrival_time"] - self.week_start).days//7
            for week in range(weeks):
                week_deals = list(filter(lambda d: d["arrival_time"] <=
                                         self.deals_closed[week]["arrival_time"] +
                                         datetime.timedelta(
                                             days=7 * (week + 1)),
                                         self.deals_closed))
                if len(week_deals) >= 10:
                    bonus += 100000
        return (self.agent["agent_id"], len(self.deals_closed),
                revenue, len(self.deals_closed)*10000, bonus)


def pick_agent(agents, customer):
    """
    Choose the best agent for customer
    """
    agents.sort(
        key=lambda a: a.agent["expertise"][customer["interest"]] + a.agent["rating"], reverse=True)
    return agents.pop(0)
