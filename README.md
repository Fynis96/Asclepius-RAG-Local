## Root Directory
- Asclepius/
    - README.md
    - .gitignore
    - docker-compose.yml
    - docker-compose.prod.yml
    - .env
    - api/
        - alembic/
        - app/
            - api/
                - endpoints/
                    - auth.py
                - deps.py
            - core/
                - config.py
                - database.py
                - security.py
            - crud/
                - user.py
            - models/
                - user.py
            - schemas/
                - user.py
            - main.py
        - alembic.ini
        - Dockerfile
        - requirements.txt
    - frontend/
        - node_modules/
        - public/
        - src/
        - .vite.config.js
        - README.md
        - package.json
        - index.html
        - Dockerfile
        - .gitignore
        - .eslintrc.cjs
    - postgres_data/
    - qdrant_data/
        

Frontend: React - TailwindCSS
Backend: FastAPI - Ollama
DBS: PostgreSQL - Qdrant - Minio