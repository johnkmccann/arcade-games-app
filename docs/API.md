# API Endpoint Reference

## Base URL
The base URL for all API requests is `https://api.arcade-games-app.com/v1`

## Authentication
All endpoints require authentication. Use the following header:
```
Authorization: Bearer {token}
```

## Endpoints

### 1. **Get All Games**
- **Endpoint:** `/games`
- **Method:** `GET`
- **Description:** Retrieves a list of all games.

### 2. **Get Game by ID**
- **Endpoint:** `/games/{id}`
- **Method:** `GET`
- **Description:** Retrieves details of a game by its ID.
- **Parameters:**  
  `{id}` - The unique identifier of the game.

### 3. **Create New Game**
- **Endpoint:** `/games`
- **Method:** `POST`
- **Description:** Creates a new game entry.
- **Body Parameters:**  
  - `name` (string, required)
  - `genre` (string, required)
  - `releaseDate` (string, required, format: YYYY-MM-DD)

### 4. **Update Game**
- **Endpoint:** `/games/{id}`
- **Method:** `PUT`
- **Description:** Updates an existing game.
- **Parameters:**  
  `{id}` - The unique identifier of the game.
- **Body Parameters:**  
  - `name` (string, optional)
  - `genre` (string, optional)
  - `releaseDate` (string, optional, format: YYYY-MM-DD)

### 5. **Delete Game**
- **Endpoint:** `/games/{id}`
- **Method:** `DELETE`
- **Description:** Deletes a game by its ID.
- **Parameters:**  
  `{id}` - The unique identifier of the game.

### 6. **Search Games**
- **Endpoint:** `/games/search`
- **Method:** `GET`
- **Description:** Searches for games based on a query.
- **Query Parameters:**  
  - `query` (string, required) - The search term used to find games.

### 7. **Get User's Favorite Games**
- **Endpoint:** `/users/{userId}/favorites`
- **Method:** `GET`
- **Description:** Retrieves a list of favorite games for a user.
- **Parameters:**  
  `{userId}` - The unique identifier of the user.

### 8. **Add Game to Favorites**
- **Endpoint:** `/users/{userId}/favorites`
- **Method:** `POST`
- **Description:** Adds a game to the user's favorites list.
- **Parameters:**  
  `{userId}` - The unique identifier of the user.
- **Body Parameters:**  
  - `gameId` (string, required) - The unique identifier of the game being added.

### 9. **Remove Game from Favorites**
- **Endpoint:** `/users/{userId}/favorites/{gameId}`
- **Method:** `DELETE`
- **Description:** Removes a game from the user's favorites list.
- **Parameters:**  
  `{userId}` - The unique identifier of the user.  
  `{gameId}` - The unique identifier of the game being removed.

---

### Error Handling
- **404 Not Found:** The requested resource could not be found.
- **401 Unauthorized:** Invalid authentication credentials.
- **400 Bad Request:** Invalid input provided.

### Response Format
All responses will be in JSON format.

### Rate Limiting
API requests are limited to 100 requests per hour per user. Contact support for increased limits.