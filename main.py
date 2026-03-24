# main.py
from dotenv import load_dotenv
from agent import ReActAgent

load_dotenv()


def run_task(agent, task_name, question):
    print("\n" + "#" * 80)
    print(task_name)
    print("#" * 80)

    answer = agent.execute(question)

    print("\nFINAL ANSWER:")
    print(answer)
    print("#" * 80 + "\n")


def main():
    agent = ReActAgent(model="gpt-4o-mini", max_steps=5)

    task1 = "What fraction of Japan's population is Taiwan's population as of 2025?"
    task2 = "Compare the main display specs of iPhone 15 and Samsung S24."
    task3 = "Who is the CEO of the startup 'Morphic' AI search?"

    run_task(agent, "TASK 1", task1)
    run_task(agent, "TASK 2", task2)
    run_task(agent, "TASK 3", task3)


if __name__ == "__main__":
    main()