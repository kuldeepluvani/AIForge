import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from clients.ollama_client import call_llama_api_chat, call_llama_api


def agentA(model_name, conversation):
    """Agent A's conversation"""
    agent_a = call_llama_api_chat(messages=conversation, model=model_name)

    return agent_a

def agentB(model_name, conversation):
    """Agent B's conversation"""
    agent_b = call_llama_api(prompt=conversation, model=model_name)

    return agent_b


def conversation_consolidation(agent_a_response, agent_b_response, conversation: list = []):
    """Consolidate the responses from Agent A and Agent B

        Agent A: Trained to be decision making model
        Agent B: Trained to be an assistant node for communication
    """
    if agent_a_response:
        conversation.append({"role": "assistant", "content": agent_a_response})
    if agent_b_response:
        conversation.append({"role": "user", "content": agent_b_response})

    return conversation


if __name__ == "__main__":
    model_name = "llama2"
    conversation = [{"role": "user", "content": "Your job is to quiz taker and quiz answer giver. If you are getting asked a question answer it and ask another question. Everytime if the answer is correct then increase the difficulty of the question"},]

    for _ in range(4):
        agent_a_response = agentA("llama2", conversation)
        # agent_a_response = "AGENT A"
        conversation = conversation_consolidation(agent_a_response, None, conversation)

        agent_b_response = agentB("gemma", agent_a_response)
        # agent_b_response = "AGENT B"
        conversation = conversation_consolidation(None, agent_b_response, conversation)


    print(conversation)
