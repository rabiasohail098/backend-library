from fastapi import FastAPI, HTTPException, Depends
import psycopg2
from database import get_db_connection
from pydantic import BaseModel
from typing import List, Optional
import logging
from passlib.context import CryptContext

# 🔧 Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔐 Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 📌 FastAPI App
app = FastAPI()

# 📌 User Schema
class User(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: Optional[str] = None  # Make email optional
    username: Optional[str] = None
    password: str  # Password is required


# 📌 Book Schema
class Book(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    genre: Optional[str] = None
    thumbnail: Optional[str] = None
    is_read: bool = False
    

   

# 📌 Update Book Schema
class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    thumbnail: Optional[str] = None
    is_read: Optional[bool] = None


# WishlistItem model
class WishlistItem(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    book_title: str

# ✅ Add to Wishlist Route
@app.post("/wishlist")
def add_to_wishlist(item: WishlistItem):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if the book exists in the books table
        cursor.execute("SELECT id FROM books WHERE title ILIKE %s", (item.book_title,))
        book = cursor.fetchone()

        # If book not found in local database, add it
        if not book:
            cursor.execute(
                "INSERT INTO books (title, author, thumbnail) VALUES (%s, %s, %s)",
                (item.book_title, "Unknown", "https://via.placeholder.com/150")
            )
            conn.commit()
            cursor.execute("SELECT id FROM books WHERE title ILIKE %s", (item.book_title,))
            book = cursor.fetchone()

        # Check if the user exists in the users table
        if item.username:
            cursor.execute("SELECT username FROM users WHERE username ILIKE %s", (item.username,))
            user = cursor.fetchone()
            if not user:
                logger.error(f"User not found: {item.username}")
                raise HTTPException(status_code=404, detail="User not found")
        elif item.email:
            cursor.execute("SELECT email FROM users WHERE email ILIKE %s", (item.email,))
            user = cursor.fetchone()
            if not user:
                logger.error(f"Email not found: {item.email}")
                raise HTTPException(status_code=404, detail="Email not found")
        else:
            raise HTTPException(status_code=400, detail="Either username or email is required")

        # Insert into wishlist
        if item.email:
            cursor.execute(
                "INSERT INTO wishlist (username, email, book_title) VALUES (%s, %s, %s)",
                (item.username, item.email, item.book_title)
            )
        else:
            cursor.execute(
                "INSERT INTO wishlist (username, book_title) VALUES (%s, %s)",
                (item.username, item.book_title)
            )
        conn.commit()
        return {"status": "success", "message": "Book added to wishlist!"}
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# ✅ Get Wishlist Route
@app.get("/wishlist/{identifier}")
def get_wishlist(identifier: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if the identifier is a username or email
        cursor.execute("SELECT username FROM users WHERE username ILIKE %s OR email ILIKE %s", (identifier, identifier))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Fetch wishlist items
        cursor.execute("SELECT book_title FROM wishlist WHERE username ILIKE %s OR email ILIKE %s", (identifier, identifier))
        wishlist = cursor.fetchall()
        return {"status": "success", "wishlist": [item[0] for item in wishlist]}
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# ✅ Signup Route
@app.post("/signup")
def signup(user: User):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s OR username = %s", (user.email, user.username))
        if cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=400, detail="User already exists!")

        # Hash the password
        hashed_password = pwd_context.hash(user.password)

        # Insert User
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (user.username, user.email, hashed_password))
        
        conn.commit()
        conn.close()
        return {"status": "success", "message": "User registered successfully!"}

    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Unexpected server error")


# ✅ Login Route
@app.post("/login")
def login(user: LoginRequest):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get user from database using email or username
        if user.email:
            cursor.execute("SELECT password FROM users WHERE email = %s", (user.email,))
        elif user.username:
            cursor.execute("SELECT password FROM users WHERE username = %s", (user.username,))
        else:
            raise HTTPException(status_code=400, detail="Email or username is required")
        
        result = cursor.fetchone()
        
        if result:
            stored_password = result[0]

            # Verify password
            if pwd_context.verify(user.password, stored_password):
                return {"status": "success", "message": "Login successful"}
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")
        
        raise HTTPException(status_code=401, detail="Invalid credentials")

    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Unexpected server error")
    
# ✅ Add Book Route
@app.post("/books")
def add_book(book: Book):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO books (title, author, year, genre, thumbnail, is_read) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                       (book.title, book.author, book.year, book.genre, book.thumbnail, book.is_read))
        
        book_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        return {"status": "success", "message": "Book added successfully!", "book_id": book_id}

    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")


# ✅ Update Book Route
@app.put("/books/{book_title}")
def update_book(book_title: str, book: UpdateBook):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if book exists
        cursor.execute("SELECT id FROM books WHERE title = %s", (book_title,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Book not found")

        # Update book details
        update_query = "UPDATE books SET "
        update_values = []
        if book.title:
            update_query += "title = %s, "
            update_values.append(book.title)
        if book.author:
            update_query += "author = %s, "
            update_values.append(book.author)
        if book.year:
            update_query += "year = %s, "
            update_values.append(book.year)
        if book.genre:
            update_query += "genre = %s, "
            update_values.append(book.genre)
        if book.thumbnail:
            update_query += "thumbnail = %s, "
            update_values.append(book.thumbnail)
        if book.is_read is not None:
            update_query += "is_read = %s, "
            update_values.append(book.is_read)

        # Remove trailing comma and add WHERE clause
        update_query = update_query.rstrip(", ") + " WHERE title = %s"
        update_values.append(book_title)

        cursor.execute(update_query, update_values)
        conn.commit()
        conn.close()
        
        return {"status": "success", "message": "Book updated successfully!"}

    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")


# ✅ Delete Book Route
@app.delete("/books/{book_title}")
def delete_book(book_title: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if book exists
        cursor.execute("SELECT id FROM books WHERE title = %s", (book_title,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Book not found")

        # Delete the book
        cursor.execute("DELETE FROM books WHERE title = %s", (book_title,))
        conn.commit()
        conn.close()
        
        return {"status": "success", "message": "Book deleted successfully!"}

    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")


# ✅ Fetch All Books Route
@app.get("/books", response_model=List[Book])
def get_books():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT title, author, year, genre, thumbnail, is_read FROM books")
        books = cursor.fetchall()
        
        conn.close()
        
        return [Book(title=row[0], author=row[1], year=row[2], genre=row[3], thumbnail=row[4], is_read=row[5]) for row in books]

    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")


# ✅ Search Books Route
@app.get("/books/search")
def search_books(query: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT title, author, year, genre, thumbnail, is_read FROM books WHERE title ILIKE %s OR author ILIKE %s", (f"%{query}%", f"%{query}%"))
        books = cursor.fetchall()
        
        conn.close()
        
        return [Book(title=row[0], author=row[1], year=row[2], genre=row[3], thumbnail=row[4], is_read=row[5]) for row in books]

    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")


# ✅ Display Statistics Route
@app.get("/stats")
def get_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total books
        cursor.execute("SELECT COUNT(*) FROM books")
        total_books = cursor.fetchone()[0]
        
        # Percentage read
        cursor.execute("SELECT COUNT(*) FROM books WHERE is_read = TRUE")
        read_books = cursor.fetchone()[0]
        percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
        
        conn.close()
        
        return {
            "status": "success",
            "total_books": total_books,
            "percentage_read": round(percentage_read, 2)
        }

    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")