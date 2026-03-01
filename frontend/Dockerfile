# Use an official Node.js runtime as a parent image
FROM node:14 AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React application
RUN npm run build

# Start with a lightweight web server for serving the build
FROM nginx:alpine

# Copy build files from the previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Command to run the web server
CMD ["nginx", "-g", "daemon off;"]