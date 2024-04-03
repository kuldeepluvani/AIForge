from crewai import Agent
from langchain_community.llms import Ollama  # Replace with Gemma if available
from langchain.prompts import TextPromptTemplate


class AgentFactoryAgent(Agent):
    """
    This agent acts as a factory for creating new agents based on instructions from Optimus Prime.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.god_operator_id = kwargs.get("god_operator_id")
        self.ollama = Ollama(model="llama2")

    def run(self, messages):
        # Check for messages from God Operator
        for message in messages:
            if message.sender == self.god_operator_id and message.data.get("action") == "create_agent":
                # Extract details for new agent
                role = message.data.get("role")
                goal = message.data.get("goal")
                backstory = message.data.get("backstory")

                # Create and register the new agent, leveraging the local Ollama model
                new_agent = Agent(role=role, goal=goal, backstory=backstory)
                new_agent.add_tool(self.ollama)
                self.crew.add_agent(new_agent)

                # Send confirmation message to God Operator
                self.send_message(self.god_operator_id, data={"message": f"Created agent with role: {role}, goal: {goal}"})


class GodOperatorAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_factory_id = kwargs.get("agent_factory_id")
        self.llm = Ollama("gemma")  # Replace with "gemma" if Gemma is available

    def run(self, messages):
        for message in messages:
            prompt = message.data.get("prompt")
            if prompt:
                required_agents, agent_details = self.analyze_prompt(prompt)
                for role, goal, backstory in agent_details:
                    self.send_agent_creation_request(role, goal, backstory)

    def analyze_prompt(self, prompt):
        # Prompt template for Gemma (replace with your desired prompt structure)
        prompt_template = TextPromptTemplate(
            inputs=[prompt],
            instructions="Given a prompt about running a crew, identify the types of agents (roles) needed. "
                         "For each role, provide a short description of its goal and backstory."
        )

        # Leverage Gemma or another LLM to analyze the prompt
        analysis_result = self.llm.run(prompt_template)
        analysis_text = analysis_result.outputs[0].text.strip()

        # Parse the analysis result (replace with logic to extract roles, goals, backstories)
        required_agents = []
        agent_details = []
        for line in analysis_text.splitlines():
            if line.startswith("- "):
                role = line[2:].strip()
                goal, backstory = self.generate_agent_info(role)  # Existing function
                agent_details.append((role, goal, backstory))

        return required_agents, agent_details


if __name__ == "__main__":
    # Replace with your CrewAI details
    GOD_OPERATOR_AGENT_ID = "YOUR_GOD_OPERATOR_AGENT_ID"
    AGENT_FACTORY_AGENT_ID = "YOUR_AGENT_FACTORY_AGENT_ID"

    # Initialize and run agents (adjust based on your CrewAI setup)
    factory_agent = AgentFactoryAgent(god_operator_id=GOD_OPERATOR_AGENT_ID)
    factory_agent.run()

    operator_agent = GodOperatorAgent(agent_factory_id=AGENT_FACTORY_AGENT_ID)
    operator_agent.run(messages={"prompt": "I want to understand the environmental impact of a new product launch. I need to analyze market trends, potential regulations and calculate the carbon footprint."})
