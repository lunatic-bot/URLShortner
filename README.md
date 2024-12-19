# URLShortener

A FastAPI-based URL shortening service that allows users to generate short URLs for their long links, with optional features like custom URLs, expiration dates, and analytics.

---

## Features

- **Shorten URLs**: Generate short URLs for any long URL.
- **Custom Short URLs**: Option to provide a custom alias for the short URL.
- **Expiration Date**: Set an expiration date for each short URL.
- **Analytics**: Track the number of times a short URL has been accessed.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/URLShortener.git
   cd URLShortener
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:

   ```bash
   alembic upgrade head
   ```

5. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

The application will be available at `http://127.0.0.1:8000`.

---

## API Endpoints

### 1. Create Short URL

**POST** `/shorten`

Request Body:

```json
{
  "original_url": "https://example.com",
  "custom_short": "custom_alias", // optional
  "expiration_date": "2024-12-31T23:59:59" // optional
}
```

Response:

```json
{
  "original_url": "https://example.com",
  "short_url": "http://127.0.0.1:8000/custom_alias",
  "access_count": 0,
  "expiration_date": "2024-12-31T23:59:59"
}
```

### 2. Redirect to Original URL

**GET** `/{short_url}`

Redirects the user to the original URL.

Response:

- 404 if the short URL does not exist.
- 410 if the short URL has expired.

### 3. Get URL Analytics

**GET** `/analytics/{short_url}`

Response:

```json
{
  "original_url": "https://example.com",
  "short_url": "custom_alias",
  "access_count": 10,
  "expiration_date": "2024-12-31T23:59:59"
}
```

---

## Database

### URLMapping Table

| Column          | Type     | Description                    |
| --------------- | -------- | ------------------------------ |
| id              | Integer  | Primary Key                    |
| original_url    | String   | The original long URL          |
| short_url       | String   | The generated or custom alias  |
| access_count    | Integer  | Tracks how many times accessed |
| expiration_date | DateTime | Optional expiration date       |

---

## Optional Enhancements

- **Custom Short URL**: Allow users to specify a custom alias for the short URL.
- **Expiration Date**: Support URLs that expire after a specific date/time.
- **Analytics**: Track and retrieve access counts for each short URL.

---

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request with your improvements or bug fixes.

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add a feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgements

- Built with [FastAPI](https://fastapi.tiangolo.com/).
- Inspired by popular URL shortener services like Bitly and TinyURL.
