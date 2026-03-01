# Development Environment Setup Instructions

## System Requirements
- **Operating System:** Linux, MacOS, or Windows.
- **Node.js:** Ensure you have Node.js (version 14.x or later) installed.
- **NPM:** Node Package Manager (comes with Node.js).
- **Git:** Required to clone the repository and basic version control.

## Steps to Set Up

1. **Clone the Repository**  
   Open your terminal or command prompt and run the following command:  
   ```bash  
   git clone https://github.com/johnkmccann/arcade-games-app.git  
   ```  
   Navigate into the cloned directory:  
   ```bash  
   cd arcade-games-app  
   ```  

2. **Install Dependencies**  
   Make sure you're in the project directory and run:  
   ```bash  
   npm install  
   ```  
   This command will install all the required packages listed in `package.json`.

3. **Run the Application**  
   After the dependencies are installed, you can run your application with:  
   ```bash  
   npm start  
   ```  
   By default, it should be accessible at `http://localhost:3000`.

4. **Development Tools**  
   It's also recommended to use a code editor like Visual Studio Code. You may want to install the following extensions for better development experience:
   - ESLint
   - Prettier
   - Live Server (for real-time preview)

5. **Testing**  
   To run tests, simply run:  
   ```bash  
   npm test  
   ```  
   This command will execute your test suite and give you feedback on the results.

## Additional Notes
- Ensure your Node.js and NPM versions are up to date to avoid compatibility issues.
- Refer to the project documentation for specific configurations and advanced setups.

## Troubleshooting
- If you encounter any issues during setup, feel free to check the issues section of the GitHub repository or contact the authors for assistance.