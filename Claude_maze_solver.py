import ASCIImaze, os, json, uuid, datetime, re
import anthropic

""" This is a simple terminal step by step interaction between the user, Claude, and the ASCIImaze. User will be prompted every turn in the terminal if they would like to add some feedback or anything else. If you see the error "incorrect input (""), try again" taht means Claude didn't use a tool. You may want to add in a prompt or set a system prompt to help avoid this from happening. At this time, it does not log or write any kind of file so this interaction is for demonstation purposes and you can enhance it as you'd like. Added ability to read and write a JSON file for conversation saving and continuation. """

# Initialize Anthropic client (you'll need to set up your API key. Currently, this look at your environment variables for "ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Define Claude move tool
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

# Print helper functions
print(
    """Prompt 'q' to quit.\n\nInclude 'force: x' in your prompt where x is the direction to help Claude make a move if it's having a hard time using the tool. Will be delayed a turn.\n-------------\n\n"""
)


# Load conversation. Disabling for now until code is implemented to resume maze moves.
def load_conversation(disabled: bool = True) -> list:
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
def write_conversation() -> None:
    # Writing to a JSON file
    with open(conv_json, "w") as json_file:
        json.dump(messages, json_file, indent=4)
    return


def get_user_input(maze: str = "", role: str = "user") -> None | str:
    # user = "Let's try and solve this maze:"
    user = input("User prompt: ")
    if user == "q":
        return "q"
    elif maze:
        messages.append(
            {"role": role, "content": f"User response: {user}\nMaze: {maze}"}
        )
        print(f"\n{maze}")
    else:
        messages.append({"role": role, "content": f"User response: {user}"})


def get_llm_response() -> str:
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
            print(x.input)
    messages.append({"role": "assistant", "content": text})
    return tool


def main(**kwargs: ASCIImaze) -> None:
    # maze = ASCIImaze.Maze("maze_map2", show_moves=False, show_coords=False)
    maze = ASCIImaze.Maze(**kwargs)

    for output in maze.solve():
        # Potential feature to stop looping through maze to sidebar LLM.
        # llm_move = ""
        # while llm_move == "":

        # Generate user prompt for Claude and add it to messages
        quit_chk = get_user_input(output)
        if quit_chk == "q":
            return
        match = re.search("(force:* *)([udlrUDLR3])", messages[-1]["content"])
        write_conversation()

        # Get Claude's response
        llm_move = get_llm_response()
        # Use user forced move. Might be delayed by a turn.
        if llm_move == "" and match and len(match.regs) == 3:
            llm_move = match[2]
            print(f"(Using forced move: {llm_move})")
        write_conversation()

        # Pass Claude's move to maze
        maze.get_user_move(llm_move)
        if llm_move == "":
            print("{Claude did not return a move.}")

    # Final solved output
    get_user_input(maze.output)
    write_conversation()

    # Get Claude's response
    get_llm_response()
    write_conversation()

    # Continue conversation after maze is completed.
    while True:
        # Generate user prompt for Claude and add it to messages. This is after the maze is completed so this can be a good opportunity to reflect on how it went.
        quit_chk = get_user_input()
        if quit_chk == "q":
            return
        write_conversation()

        # Get Claude's response
        get_llm_response()
        write_conversation()


if __name__ == "__main__":
    # Use key word arguments
    main(maze_map="maze_map2", show_moves=False, show_coords=False)
