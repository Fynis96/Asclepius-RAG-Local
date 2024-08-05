Dockerized RAG App
Current Use Case: Quickly solve Appeals tasks.

Problem: Provided 3 documents pertaining to patient.  MR, Labs, Correspondance.
Correspondance details why patients claim was denied.
Find evidence from all three documents to say its wrong, help fill in template for email communications towards appealing the claim denial.

Constraint: No Third Party sources injesting PHI/PII, so locally ran model, thus Ollama.
Dockerized to easily move across hardware from dev's local machine to a server situation.
Hopefully dev machine is powerful enough on Demo Day to pull the traffic and not break

Future Consideration:
- If load balancing becomes an issue, will add RabbitMQ and 1-2 workers to the DockerCompose.

Backend:
FastAPI
Llama-Index for document indexing and retrieval
Alembic for database migrations
SQLAlchemy  for ORM
Pydantic for data validation
Ollama (Dockerized) for local language model hosting
    - Pull Default Models after healthcheck on startup (Maybe have code do and wait for this)
        - Options to pull other models(?) - unimportant

- Endpoints:
    - auth.py
        - Login
        - Logout
        - Refresh Token
    - knowledgebase.py 
        - Create KB (user=Depends(get_current_user), kb_name, kb_desc(optional), )
        - Get KBS ()
        - Get KB
        - Update KB
        - Delete KB
        - Async Index KB
        - Async Create Document
        - Get Documents
        - Get Document
        - Delete Document
        - Async Index Document (Between letting user do so, and doing by default)
        - Get Indexes
        - Get Index
        - Delete Index
    - user.py
        - Read Users Me (get current user)
        - Create User
        - Get Users
        - Get User
        - Delete User
        - Update User
    - chat.py
        - Create Chatbot (Create/Config and add to postgres)
        - Delete Chatbot
        - Update Chatbot
        - Get Chatbot
        - Get Chatbots
        - Create Chat (Take config from postgres and start loading into memory through llamaindex, will be used by frontend when user goes to the actual chat ui.)
        - Async Qeury (chat_id, content, role) returns chatbot response
        - Async Query Streaming(? for streamed messages)
        - Get Chat
        - Get Chats
        - Delete Chat
        - Update Chat


Frontend:

    React Base (Reminder to sanitize user input)
    - Navbar
        - Login/Register
            - Simple OAuth2 situation involving JWT, User/Hashed Pass.
        (Protected Routes, only User with active token can do anything with these routes)
        - Dashboard
            - User Profile/Settings
                - Change Password
                - Future settings here as well (darkmode, etc.)
            - Knowledgebases
            Create new/Delete
                - Documents
                Upload/Delete/Index (or index by default)
                    Validate documents being uploaded for size/file type.
            - Chatbots (Can use indexed documents) 
                - Chats
    TailwindCSS (Quick and Easy good views.)

Persistance:
    
    Qdrant - VectorDB
        - Documents indexed/embedded, vectors sent here and stored/attached to document/documentID
    Minio - Buckets/S3 
        - Document Store, Tied to KnowledgeBase/the ID
            - Validate/Limit from both backend and frontend
    PostgreSQL - SQL
        - User
            - ID
            - Role
            - Email
            - Hashed Password
            - Refresh Token
            - IsActive
            - knowledgebases
            - chatbots
        - Knowledebase
            - ID
            - name
            - description
            - user_id
            - user
            - documents
        - Document
            - ID
            - filename
            - file_path
            - file_type
            - knowledgebase_id
            - knowledgebase
            - is_indexed (default=False)
            - index_id (nullable)
            - index
        - Index(?)
            - ID
            - Document/docid (doc indexed from)
            - location/ref/misc
        - Chatbot
            - ID
            - Model (default=llama3.1)
            - Temperature (default=0.2)
            - isActive (default=False)
            - EngineType?(Query Engine, etc.)
            - Index/embedding/vectorizedDoc (nullable)
        - ChatMessage
            - ID
            - Content
            - Role
            - CreatedAt
            - ChatbotID
            - chatbot
        
    

Secrets:
    .env
        - Postgres user/pass/dbs/port
        - Minio user/pass/port
        - Qdrant user/pass/port
        - JWT Secret Key for hashing


Features/UserStories:
    MVP:
        - User logs in, easily able to upload document, index, and start workflow/chat to get task done regarding the document
            - User has multiple pre-tested prompts/queries that work towards this task
    Would Be Nice:
        - document pre-processing pipeline (using llama_indexes has worked so far)
        - Feedback Loop for Continuous improvment
    Meh:








Random Thoughts:
- Patient Extractor using Pydantic model?: https://docs.llamaindex.ai/en/stable/examples/workflow/reflection/
    - Equally important for all other keywords as well, generally parsing and grabbing this and the most relevant info first before querying against the already messy data which is that of the parsed pdfs
- Workflows seem to be right in ballpark of aims I was going for on this app
    - Multi Stage configurable pipelines (i.e. Appeals Pipeline):
        - Document intake & validation
        - Automatic categorization of denial reasons (OOh, during embedding, chunking, reranking, we can have this consideration in mind)
        - Evidence gathering from multiple sources
        - response generation with human-in-the-loop approval
- We can make the workflows more powerful with the use of a more powerful AI (GPT, Claude), without sending important or Secure PHI to these sources.
- Ollama Multi-modal: https://docs.llamaindex.ai/en/stable/examples/multi_modal/ollama_cookbook/
- Semantic Chunker (chooses chunk size): https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_chunking/
    - Pair with reranker concept/relevance check
- RERANKER
- Implement hybrid search combining keyword and semantic search
- Add support for multi-modal inputs (text, images, audio)
- Implement caching mechanisms (e.g., Redis) for frequently accessed data
- Add input sanitization and validation on both frontend and backend
- Implement proper HTTPS/TLS configuration
- Consider adding two-factor authentication (2FA) for user accounts
- Implement application performance monitoring (APM)
- Implement circuit breakers for external service calls
- Add retry mechanisms for transient failures
- Develop a comprehensive error handling strategy across the application
- Set up automated builds and deployments
- Implement code quality checks (linting, formatting)
- Add security scanning for dependencies and Docker images
- Develop data governance policies and ensure compliance (e.g., GDPR, HIPAA)
- Add features for data subject access requests and right to be forgotten
- Figure out how K8's would work in this situation in terms of scaling?
- In the Demo, have 4 out of the 5 examples already indexed and ready to go, chat histories filled with acurate info etc. Use 5th example to run through the flow after showing some successes, use one more success chat history if live example bombs
- Implement other tools that can assist with the appeals process
- Document/PDF viewer with highlighting & Annotations (LOL, this ones funny, it would be AMAZING as a feature, but the work and testing to get this one going may take a bit if pre-existing libraries/services don't already exist) Some ideas for this though, when injesting document and chunking, attach location data that the llm doesn't take in, but can be used to create a bounding box (4 points) to give just a specific view of the document? Just a thought
- Guided Workflow for creating/managing appeals?
- machine learning model for predicting appeal success probabilty(?)
- knowledge base of successful appeals for reference
- Advanced Security measures
    - end-to-end encrpytion
    - MFA
    - RBAC
- Batch processing support (Upload alot of folders, get default workflow responses over time, be able to re-run specific batch that didn't provide good results)
- Implement rate limiting and request throttling