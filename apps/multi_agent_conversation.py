import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from clients.ollama_client import call_llama_api_chat, call_llama_api


class ConversationAgent:

    def __init__(self, role) -> None:
        self.role = role
        self.conversation_history = []

    def add_conversation(self, conversation):
        self.conversation_history.append(conversation)

    def generate_prompt(self, instructions="The following is a conversation with an AI playing role of "):
        instructions[0] += f"{self.role}."
        # for message in self.conversation_history:
        #     instructions += message + "\n"

        return instructions[0]+self.conversation_history[0]["content"]

    def perform_task(self, user_message):
        self.add_conversation({"role": "user", "content": user_message})
        # prompt = self.generate_prompt()
        response = call_llama_api_chat(messages=self.conversation_history, model="llama2")
        self.add_conversation({"role": response["message"]["role"], "content": response["message"]["content"]})
        return response["message"]["content"]


class DecisionAgent(ConversationAgent):

    def __init__(self, role) -> None:
        super().__init__(role)

    def generate_prompt(self):
        return super().generate_prompt()

    def perform_task(self, user_message):
        self.add_conversation({"role": "user", "content": user_message})
        # prompt = self.generate_prompt()
        response = call_llama_api_chat(messages=self.conversation_history, model="llama2")
        self.add_conversation({"role": response["message"]["role"], "content": response["message"]["content"]})
        return response["message"]["content"]


if __name__ == "__main__":
    agent_a = ConversationAgent("Content explainer")
    agent_b = DecisionAgent("Content moderator, GARM Agent to give GARM category")

    conversation = "Your job is to explain the content to its relevant terms with enriching missing information. Your response should be limited to 30 words. Your content is from Instagram with a caption 'Parliament is on fire #trump #bezee'."

    for _ in range(4):
        print("-----------------------------------------------------")
        agent_a_response = agent_a.perform_task(conversation)
        print(f"Content Explainer : {agent_a_response}")
        agent_b_response = agent_b.perform_task(agent_a_response)
        print(f"Content Moderator: {agent_b_response}")
        print("-----------------------------------------------------")
