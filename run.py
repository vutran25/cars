"""
Car sales.
"""
import statistics
#from dealer import AGENTS
from dealer.agent import Agent
from dealer import AGENTS
from data.customers import customers


CUSTOMERS = customers(100)


class Run(object):
    """
    Run the sales.
    """

    def sales(self):
        """
        Simulate sales using test data and print out customer and agent reports.
        """
        wait_times = []
        for agent in AGENTS:
            Agent.innit(agent)

        for customer in CUSTOMERS:
            agent, time = Agent.get(customer)
            wait_times.append(time)
        print("{:8} {:8} {:8}".format("Mean", "Median", "Standard deviation"))
        print("{:<8.2f} {:<8} {:<8.2f} \n".format(
            statistics.mean(wait_times),
            statistics.median(wait_times), statistics.stdev(wait_times)))
        print("{:<7}  {:<7}  {:<20}  {:<15}  {:<20}".format(
            "ID", "DEALS", "REVENUE", "COMMISSION", "BONUS"))
        for agent in Agent.working_agents:
            agent_id, deals, revenue, commission, bonus = agent.performace_report()
            print("{:<7}  {:<6}  ${:<19,.2f}  ${:<14,.2f}  ${:<19,.2f}".format(
                agent_id, deals, float(revenue), commission, float(bonus)))


if __name__ == "__main__":
    Run().sales()
