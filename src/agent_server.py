from flask import Flask, request, Response
import json
import uuid
from langchain_core.messages import HumanMessage
from langchain_core.messages.ai import AIMessage
from agent import agent_executor
import time

app = Flask(__name__)

# format the agent response data according to GitHub App
def get_response_data(content, finish_reason=None):
    response_data = {
        "id": str(uuid.uuid4()), 
        "object": "chat.completion.chunk",
        "created": int(time.time()),  
        "model": "gpt-3.5-turbo-0125",
        "system_fingerprint": "fp_44709d6fcb",
        "choices": [{
            "index": 0,
            "delta": {
                "content": content
            },
            "logprobs": None,
            "finish_reason": finish_reason
        }]
    }
    return response_data

@app.route('/stream', methods=['POST'])
def stream_response():
    def generate_agent_response(msgs, x_github_token):
        try:
            # perform message differentiation
            msgs = [HumanMessage(content=msg) if i % 2 == 0 else AIMessage(content=msg) for i, msg in enumerate(msgs)]
            # agent executors only focus on the 'messages' key
            msgs.append(HumanMessage(content="The X-Github-Token is " + x_github_token))
            for event in agent_executor.stream({"messages": msgs}):
                # check whether the message is a tool call or an LLM response
                if 'agent' in event:
                    response_data = get_response_data(event.get('agent').get('messages')[0].content)
                else:
                    print("calling tool " + event.get('tools').get('messages')[0].name + "...")
                    response_data = get_response_data("calling tool " + event.get('tools').get('messages')[0].name + "... ")
                yield f"data: {json.dumps(response_data)}\n\n"  # Format for SSE
            final_data = get_response_data("", "stop")
            yield f"data: {json.dumps(final_data)}\n\n"
        except Exception as e:
            print(f"ERRORED WITH {e}")
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"

    x_github_token = request.headers.get('X-GitHub-Token')
    msgs = [msg['content'] for msg in request.json.get('messages', [])]
    return Response(generate_agent_response(msgs, x_github_token), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)