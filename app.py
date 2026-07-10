from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

from db.users import usermanager
from db.messages import messagemanager

from db.sessions import sessionmanager

from langchain.messages import AIMessage,HumanMessage

from ai import agent

app=FastAPI(title="AI STUDY PARTNER")

sessions=sessionmanager()
messages=messagemanager()
users=usermanager()

class ChatRequest(BaseModel):
    username:str
    session_id:str|None=None
    query:str

class ChatResponse(BaseModel):
    session_id:str
    response:str

def load_chat_history(session_id:str):
    row=messages.get_messages(session_id)
    history=[]

    for i in row:
        if i["role"]=="human":
            history.append(HumanMessage(content=i["message"]))
        else:
            history.append(AIMessage(content=i["message"]))
    return history
    

@app.get("/sessions/{username}")
def load_session(username:str):
    user=users.get_user(username)
    if user is None:
        return[]
    
    
    
    user_id=user["id"]
    
    row=sessions.get_all_sessions(user_id)

    return row

@app.get("/messages/{session_id}")
def load_chat(session_id:str):
    rows=messages.get_messages(session_id)
    return[{
        "role":row["role"],
        "message":row["message"]
    }
    for row in rows
    ]

@app.post("/chat",response_model=ChatResponse)
def chat(req:ChatRequest):
    try:
        id=users.create_user(req.username)
        
        session_id=req.session_id
        if session_id is None:
            session_id=sessions.create_session(
                user_id=id,
                title=req.query.strip()[:20]
                )

        history=load_chat_history(session_id)

        response=agent.invoke(
            {
                "messages":history+[
                    HumanMessage(content=req.query)
                ]
            }
        )
        message=response["messages"][-1].content
    

        messages.save_message(
            session_id=session_id,
            message=req.query,
            role="human",
            model="llama-3.3-70b-versatile"
            )
        messages.save_message(
            session_id=session_id,
            message=message,
            role="assistant",
            model="llama-3.3-70b-versatile"
         )

        return ChatResponse(
                session_id=session_id,
                response=message
            )
        
    except Exception as e:
            import traceback
            traceback.print_exc()  
            
            raise HTTPException(
                status_code=500,detail=str(e)
            )      
           


   





