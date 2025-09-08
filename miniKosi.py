from flask import Flask, render_template, request, jsonify, session
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import uuid
import os
import secrets

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production!

# --- Define the search tool ---
@tool
def search(query: str):
    """Call this only when you need to search for current information like weather, news, or facts you don't know."""
    if "weather" in query.lower():
        return "It is sunny and pleasant today."
    elif "news" in query.lower():
        return "Here are the latest headlines: Technology stocks are up today."
    elif "time" in query.lower():
        return "The current time is 2:30 PM."
    return f"Search results for '{query}': No specific information found, but you can provide a general response."

tools = [search]
tool_node = ToolNode(tools)

# --- Define the Google model ---
# Make sure to set your GOOGLE_API_KEY environment variable
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro", 
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")  # Set this in your environment
).bind_tools(tools)

# --- Agent function ---
def call_model(state: MessagesState):
    messages = state["messages"]
    
    # Add system guidance if this is the first message or no system message exists
    if not any(hasattr(msg, 'type') and msg.type == "system" for msg in messages):
        system_message = HumanMessage(content="""You are a helpful AI assistant. For simple greetings and casual conversation, respond directly without using tools. Only use the search tool when you need to look up current information like weather, news, or specific facts you don't know. For greetings like 'hey', 'hello', 'hi', just respond normally as a friendly assistant.""")
        messages = [system_message] + messages
    
    response = model.invoke(messages)
    return {"messages": [response]}

# --- Tool routing function ---
def should_continue(state: MessagesState):
    last_message = state["messages"][-1]
    
    # Check if the model wants to use tools
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    
    # Otherwise, end this turn
    return "end"

# --- Build the workflow ---
workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent", 
    should_continue, 
    {
        "tools": "tools",
        "end": END
    }
)
workflow.add_edge("tools", "agent")

checkpointer = MemorySaver()
app_graph = workflow.compile(checkpointer=checkpointer)

# --- Flask Routes ---
@app.route('/')
def index():
    # Initialize session if new user
    if 'thread_id' not in session:
        session['thread_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get or create thread config
        thread_config = {"configurable": {"thread_id": session['thread_id']}}
        
        # Get response from agent
        final_state = app_graph.invoke(
            {"messages": [HumanMessage(content=user_message)]},
            config=thread_config
        )
        
        # Extract the response
        response = final_state["messages"][-1]
        if isinstance(response, AIMessage):
            agent_response = response.content
        else:
            agent_response = str(response)
        
        return jsonify({
            'response': agent_response,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Error processing message: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/new_chat', methods=['POST'])
def new_chat():
    # Generate new thread ID for fresh conversation
    session['thread_id'] = str(uuid.uuid4())
    return jsonify({'status': 'success', 'message': 'New chat started'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)