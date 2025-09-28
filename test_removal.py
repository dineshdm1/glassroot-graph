import json
from openai import OpenAI
from secrets import OPENAI_API_KEY

# Set up OpenAI the new way
client = OpenAI(api_key=OPENAI_API_KEY)


def extract_task_from_conversation(conversation_data):
    """Figure out what the team was trying to do"""
    task_description = ""
    for msg in conversation_data["history"][:3]:
        content = msg.get("content", "")
        if len(content) > 50:
            task_description = content
            break

    return {
        'task': task_description,
        'original_agents': list(set(msg["name"] for msg in conversation_data["history"]))
    }


def create_reduced_team(conversation_data):
    """Remove the chattiest agent and return new team"""
    agent_talk_count = {}
    for msg in conversation_data["history"]:
        agent = msg["name"]
        agent_talk_count[agent] = agent_talk_count.get(
            agent, 0) + len(msg.get("content", ""))

    chattiest = max(agent_talk_count, key=agent_talk_count.get)
    remaining_agents = [
        agent for agent in agent_talk_count.keys() if agent != chattiest]

    return {
        'removed_agent': chattiest,
        'remaining_agents': remaining_agents
    }


def create_simple_agent(agent_name, task):
    """Create a simple agent with a role"""
    if "verification" in agent_name.lower():
        role = "You check work for mistakes."
    elif "analysis" in agent_name.lower():
        role = "You analyze data."
    elif "python" in agent_name.lower():
        role = "You write code."
    elif "terminal" in agent_name.lower():
        role = "You run commands."
    else:
        role = "You solve problems."

    return {
        'name': agent_name,
        'role': role
    }


def run_openai_test(agents, task):
    """Run one quick test with OpenAI"""
    print("Starting team conversation...")

    conversation = []

    for turn in range(3):
        agent = agents[turn % len(agents)]

        context = f"Task: {task}\n\n"
        if conversation:
            context += "Previous messages:\n"
            for msg in conversation[-2:]:
                context += f"{msg['name']}: {msg['content']}\n"

        context += f"\n{agent['name']} ({agent['role']}), what's your response? Keep it short."

        try:
            # New OpenAI format
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                        "content": f"You are {agent['name']}. {agent['role']} Give short, helpful responses."},
                    {"role": "user", "content": context}
                ],
                max_tokens=80,
                temperature=0.7
            )

            content = response.choices[0].message.content.strip()
            message = {'name': agent['name'], 'content': content}
            conversation.append(message)

            print(f"{agent['name']}: {content}")

        except Exception as e:
            print(f"Error with {agent['name']}: {e}")
            break

    return conversation


# Test it
if __name__ == "__main__":
    print("Testing one conversation without the chattiest agent...")

    with open("who_when_data/Who&When/Algorithm-Generated/1.json") as f:
        data = json.load(f)

    task_info = extract_task_from_conversation(data)
    team_info = create_reduced_team(data)

    print(f"Original team failed at this task.")
    print(f"Removing chattiest agent: {team_info['removed_agent']}")
    print(f"Testing with: {team_info['remaining_agents']}")
    print()

    agents = [create_simple_agent(name, task_info['task'])
              for name in team_info['remaining_agents']]

    conversation = run_openai_test(agents, task_info['task'])

    print(f"\nTest complete. The team had {len(conversation)} exchanges.")
