import ASCIImaze, os, json, uuid, datetime
import anthropic

""" This is a simple terminal step by step interaction between the user, Claude, and the ASCIImaze. User will be prompted every turn in the terminal if they would like to add some feedback or anything else. If you see the error "incorrect input (""), try again" taht means Claude didn't use a tool. You may want to add in a prompt or set a system prompt to help avoid this from happening. At this time, it does not log or write any kind of file so this interaction is for demonstation purposes and you can enhance it as you'd like. Added ability to read and write a JSON file for conversation saving and continuation. """

# Initialize Anthropic client (you'll need to set up your API key. Currently, this look at your environment variables for "ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

tools = [
    {
        "name": "maze_move",
        "description": "Input for maze. Only one character.",
        "input_schema": {
            "type": "object",
            "properties": {
                "move": {
                    "type": "string",
                    "description": "One character input for the maze",
                }
            },
            "required": ["move"],
        },
    }
]
# Conversation stored here. Change name to start or resume a chat session. Continuing conversations will need to reinput the previous moves which hasn't been implemented yet.
conversation_name = f"Claude_maze_test_{datetime.date.today()}_{uuid.uuid4().hex}.json"
messages = []

# Get current directory
path = os.path.dirname(os.path.abspath(__file__))
conv_json = path + os.sep + "conversations" + os.sep + conversation_name


# Load conversation. Disabling for now until code is implemented to resume maze moves.
def load_conversation(disabled=True):
    if not disabled:
        # Load JSON file
        with open(conv_json, "r") as json_file:
            messages = json.load(json_file)
            for message in messages:
                print(message["role"] + ": " + message["content"] + "\n")
            return messages
    return []


if os.path.exists(conv_json):
    messages = load_conversation()


# Update conversation
def write_conversation():
    # Writing to a JSON file
    with open(conv_json, "w") as json_file:
        json.dump(messages, json_file, indent=4)
    return


def get_user_input(maze="", role="user"):
    # user = "Let's try and solve this maze:"
    user = input("User prompt: ")
    messages.append({"role": role, "content": f"User response: {user}\nMaze: {maze}"})
    print(f"\n{maze}")


def get_llm_response():
    """Get a response from Claude."""
    tool = ""
    text = ""
    response = client.messages.create(
        # model="claude-3-opus-20240229",
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=0.0,
        messages=messages,
        tools=tools,
    )
    for x in response.content:
        if x.type == "text":
            text += x.text
            print(x.text)
        elif x.type == "tool_use":
            tool = x.input["move"]
            # text += str(x.input)
            print(x.input)
    messages.append({"role": "assistant", "content": text})
    # print(text)
    # print(tool)
    return tool


def main():
    maze = ASCIImaze.Maze("maze_map2", show_moves=False, show_coords=False)

    for output in maze.solve():
        # llm_move = ""
        # while llm_move == "":

        # Generate user prompt for Claude and add it to messages
        get_user_input(output)
        write_conversation()

        # Get Claude's response
        llm_move = get_llm_response()
        write_conversation()

        maze.get_user_move(llm_move)
        if llm_move == "":
            # Pass Claude's move to program
            print("{Claude did not return a move.}")

    # Final solved output
    get_user_input(maze.output)


if __name__ == "__main__":
    main()
