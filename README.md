# Arcade Games App

## Project Overview
The Arcade Games App is an interactive platform that allows users to play classic arcade games directly from their web browser. This project aims to replicate the nostalgic experience of arcade gaming while utilizing modern web technologies. The application is designed with user-friendly interfaces and engaging gameplay mechanics, making it suitable for players of all ages.

### Features
- **Multiple Games:** Includes a collection of classic arcade games such as Snake, Tetris, and Space Invaders.
- **User Accounts:** Register and maintain user profiles for a personalized experience.
- **High Scores:** Track and display high scores for all games.
- **Responsive Design:** Optimized for both desktop and mobile devices.

## Quick Start Instructions
To get started with the Arcade Games App, follow the instructions below:

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker and Docker Compose)
- [Visual Studio Code](https://code.visualstudio.com/) (recommended for dev containers)
- **VS Code Extension:** [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) (required for dev container support)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/johnkmccann/arcade-games-app.git
   cd arcade-games-app
   ```

2. **For Dev Containers (Recommended):** 
   Skip to the "Running the Application" section and choose Option 1. The dev container handles all setup automatically.

3. **For Local Development (Optional):**
   
   **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cd ..
   ```

   **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Running the Application

#### Option 1: Using Dev Containers (Recommended)
This is the easiest development experience with automatic setup:

1. **Before opening the project**, ensure Docker Desktop is running on your Mac. You can run this helper script to verify:
   ```bash
   bash scripts/ensure-docker-local.sh
   ```

2. Open the project in VS Code.
3. VS Code will detect the `.devcontainer/devcontainer.json` and prompt you to "Reopen in Container" — click it.
4. Wait for the container to build and dependencies to install (first time only, a few minutes).
5. Once ready, VS Code opens inside the container with everything pre-configured.

6. **Configure VS Code Settings (First Time Only)**
   Copy the settings template to create your local configuration:
   ```bash
   cp .vscode/settings.example.json .vscode/settings.json
   ```
   This enables test discovery for both backend (pytest) and frontend (vitest) in the Testing tab.

All dependencies are automatically installed! Start the dev servers using the **Run and Debug** tab in VS Code:

1. Open the **Run and Debug** view (Ctrl+Shift+D / Cmd+Shift+D)
2. Select **"Full Stack"** from the dropdown to run both backend and frontend
3. Or run them individually:
   - **"Backend (Uvicorn)"** — Python debug server on port 5001
   - **"Frontend (Vite Dev)"** — Vite dev server on port 5173

You can also run them manually in terminals if preferred:

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
- MongoDB: Runs automatically in the container

Code changes trigger instant hot-reload. Only rebuild the container if you change `requirements.txt` or `package.json`.

#### Option 2: Using Docker Compose (Production-like)
For testing the full containerized stack:
```bash
docker-compose -f docker-compose.prod.yml up
```

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:5001`

#### Option 3: Running Locally Without Docker

Start MongoDB separately, then:

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

### License
This project is licensed under the MIT License.