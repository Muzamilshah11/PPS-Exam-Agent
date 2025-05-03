import chainlit as cl
from all_agents import triage_agent  # assuming your agent_workflow.py is in PYTHONPATH
from agents import  Runner

# Run the app
# uv run chainlit run app.py -w

@cl.on_chat_start
async def start():
    # 1) Initialize an empty chat history list in the user session
    cl.user_session.set("chat_history", [])  # persists per session :contentReference[oaicite:0]{index=0}

    # 2) Store the triage agent for later use in on_message
    cl.user_session.set("triage_agent", triage_agent)  # lets you access triage_agent in other hooks

    # 3) Send a friendly, contextual welcome prompt
    await cl.Message(
         content=(
            "👋 Welcome! I'm your PPS (BPS‑17) Exam Agent.\n"
            "📚 Custom study plans, 📝 targeted practice, 💡 expert insights ask me anything to conquer your exam!"
        )
    ).send()  # uses Message.send() in an on_chat_start hook :contentReference[oaicite:1]{index=1}


@cl.on_message
async def main(message: cl.Message):
    # 1) Show a temporary “Thinking…” message
    thinking_msg = cl.Message(content="Thinking…")
    await thinking_msg.send()

    # 2) Retrieve and update chat history
    history = cl.user_session.get("chat_history", [])
    history.append({"role": "user", "content": message.content})

    # 3) Fetch the triage agent (in case you want to allow dynamic swapping)
    agent = cl.user_session.get("triage_agent", triage_agent)

    # 4) Run the triage workflow
    result = await Runner.run(starting_agent=agent, input=history)

    # 5) Persist updated history back into the session
    cl.user_session.set("chat_history", result.to_input_list())

    # 6) Replace “Thinking…” with the agent’s actual response
    thinking_msg.content = result.final_output
    await thinking_msg.update()

@cl.on_chat_end
async def end():
    # Optional: perform any cleanup here, e.g., logging or resource release
    # Send a farewell message to the user
    await cl.Message(
        content=(
            "🎉 Thank you for chatting with me! "
            "I hope I was able to help. "
            "Feel free to return anytime—goodbye! 👋"
        )
    ).send()

