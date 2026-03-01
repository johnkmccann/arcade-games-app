# Development Environment Setup Instructions

## System Requirements
- **Operating System:** Linux, macOS, or Windows
- **Docker Desktop:** Required for dev containers ([Download here](https://www.docker.com/products/docker-desktop))
- **VS Code:** Recommended code editor
- **Git:** Required to clone the repository

## Quick Start with Dev Containers (Recommended)

Dev Containers provide a streamlined development environment with all dependencies pre-configured.

### Steps

1. **Install Docker Desktop**
   - Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Start Docker Desktop and verify it's running

2. **Clone the Repository**
   ```bash
   git clone https://github.com/johnkmccann/arcade-games-app.git
   cd arcade-games-app
   ```

3. **Open in VS Code**
   ```bash
   code .
   ```

4. **Reopen in Container**
   - VS Code will detect `.devcontainer/devcontainer.json` and prompt: "Reopen in Container"
   - Click the button or use Command Palette: `Dev Containers: Reopen in Container`
   - Wait for the container to build and dependencies to install (first time only, takes a few minutes)
   - You'll see a message when everything is ready

5. **Run Dev Servers**
   
   All dependencies are automatically installed! In VS Code's integrated terminal, start the dev servers:

   **Terminal 1 - Backend:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --port 5001
   ```

   **Terminal 2 - Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

   Access the application:
   - Frontend: `http://localhost:5173`
   - Backend API: `http://localhost:5001`
   - MongoDB: Running automatically in the container

6. **Development Workflow**
   - Edit code normally in VS Code
   - Changes trigger hot-reload automatically
   - Only rebuild the container if you change `requirements.txt` or `package.json`

## Alternative: Local Development (Without Dev Containers)

### Prerequisites
- **Node.js** v16 or later
- **Python** v3.12 or later
- **MongoDB** (local installation or Docker)

### Setup Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/johnkmccann/arcade-games-app.git
   cd arcade-games-app
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cd ..
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Start MongoDB**
   - If installed locally, start your MongoDB service
   - Or run: `mongod`

5. **Run the Application**
   
   **Terminal 1 - Backend:**
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python -m uvicorn app.main:app --reload --port 5001
   ```

   **Terminal 2 - Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

## VS Code Recommended Extensions

When using dev containers, these extensions are automatically installed:
- **Python** (ms-python.python)
- **Pylance** (ms-python.vscode-pylance)
- **ESLint** (dbaeumer.vscode-eslint)
- **Prettier** (esbenp.prettier-vscode)
- **MongoDB** (mongodb.mongodb-vscode)

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Troubleshooting

**"Reopen in Container" option not showing:**
- Ensure VS Code Remote - Containers extension is installed
- Reload VS Code window

**Container build fails:**
- Check Docker Desktop is running
- Try: `Dev Containers: Rebuild Container`

**Port already in use:**
- Ensure no other service is running on ports 5173, 5001, or 27017
- Or modify port mappings in `.devcontainer/docker-compose.yml`

**Dependencies not installing in container:**
- Rebuild the container: `Dev Containers: Rebuild Container`


## Troubleshooting
- If you encounter any issues during setup, feel free to check the issues section of the GitHub repository or contact the authors for assistance.