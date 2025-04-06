# # from fastapi import FastAPI, HTTPException, Depends
# # import psycopg2
# # from database import get_db_connection
# # from pydantic import BaseModel
# # from typing import List, Optional
# # import logging
# # from passlib.context import CryptContext
# # import base64
# # # 🔧 Setup Logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# # # 🔐 Password Hashing
# # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # # 📌 FastAPI App
# # app = FastAPI()

# # # 📌 User Schema
# # class User(BaseModel):
# #     username: str
# #     email: str
# #     password: str

# # class LoginRequest(BaseModel):
# #     email: Optional[str] = None  # Make email optional
# #     username: Optional[str] = None
# #     password: str  # Password is required


# # # 📌 Book Schema
# # class Book(BaseModel):
# #     title: str
# #     author: str
# #     year: Optional[int] = None
# #     genre: Optional[str] = None
# #     thumbnail: Optional[bytes] = None  # Change from str to bytes
# #     is_read: bool = False

# #     class Config:
# #         json_encoders = {
# #             bytes: lambda v: base64.b64encode(v).decode('utf-8') if v else None
# #         }
    

   

# # # 📌 Update Book Schema
# # class UpdateBook(BaseModel):
# #     title: Optional[str] = None
# #     author: Optional[str] = None
# #     year: Optional[int] = None
# #     genre: Optional[str] = None
# #     thumbnail: Optional[str] = None
# #     is_read: Optional[bool] = None


# # # WishlistItem model
# # class WishlistItem(BaseModel):
# #     username: Optional[str] = None
# #     email: Optional[str] = None
# #     book_title: str

# # # ✅ Add to Wishlist Route
# # @app.post("/wishlist")
# # def add_to_wishlist(item: WishlistItem):
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
# #     try:
# #         # Check if the book exists in the books table
# #         cursor.execute("SELECT id FROM books WHERE title ILIKE %s", (item.book_title,))
# #         book = cursor.fetchone()

# #         # If book not found in local database, add it
# #         if not book:
# #             cursor.execute(
# #                 "INSERT INTO books (title, author, thumbnail) VALUES (%s, %s, %s)",
# #                 (item.book_title, "Unknown", "https://via.placeholder.com/150")
# #             )
# #             conn.commit()
# #             cursor.execute("SELECT id FROM books WHERE title ILIKE %s", (item.book_title,))
# #             book = cursor.fetchone()

# #         # Check if the user exists in the users table
# #         if item.username:
# #             cursor.execute("SELECT username FROM users WHERE username ILIKE %s", (item.username,))
# #             user = cursor.fetchone()
# #             if not user:
# #                 logger.error(f"User not found: {item.username}")
# #                 raise HTTPException(status_code=404, detail="User not found")
# #         elif item.email:
# #             cursor.execute("SELECT email FROM users WHERE email ILIKE %s", (item.email,))
# #             user = cursor.fetchone()
# #             if not user:
# #                 logger.error(f"Email not found: {item.email}")
# #                 raise HTTPException(status_code=404, detail="Email not found")
# #         else:
# #             raise HTTPException(status_code=400, detail="Either username or email is required")

# #         # Insert into wishlist
# #         if item.email:
# #             cursor.execute(
# #                 "INSERT INTO wishlist (username, email, book_title) VALUES (%s, %s, %s)",
# #                 (item.username, item.email, item.book_title)
# #             )
# #         else:
# #             cursor.execute(
# #                 "INSERT INTO wishlist (username, book_title) VALUES (%s, %s)",
# #                 (item.username, item.book_title)
# #             )
# #         conn.commit()
# #         return {"status": "success", "message": "Book added to wishlist!"}
# #     except psycopg2.Error as e:
# #         logger.error(f"Database error: {e}")
# #         raise HTTPException(status_code=500, detail=f"Database error: {e}")
# #     except Exception as e:
# #         logger.error(f"Unexpected error: {e}")
# #         raise HTTPException(status_code=500, detail=str(e))
# #     finally:
# #         conn.close()

# # # ✅ Get Wishlist Route
# # @app.get("/wishlist/{identifier}")
# # def get_wishlist(identifier: str):
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
# #     try:
# #         # Check if the identifier is a username or email
# #         cursor.execute("SELECT username FROM users WHERE username ILIKE %s OR email ILIKE %s", (identifier, identifier))
# #         user = cursor.fetchone()
# #         if not user:
# #             raise HTTPException(status_code=404, detail="User not found")

# #         # Fetch wishlist items
# #         cursor.execute("SELECT book_title FROM wishlist WHERE username ILIKE %s OR email ILIKE %s", (identifier, identifier))
# #         wishlist = cursor.fetchall()
# #         return {"status": "success", "wishlist": [item[0] for item in wishlist]}
# #     except psycopg2.Error as e:
# #         logger.error(f"Database error: {e}")
# #         raise HTTPException(status_code=500, detail="Database error")
# #     except Exception as e:
# #         logger.error(f"Unexpected error: {e}")
# #         raise HTTPException(status_code=500, detail=str(e))
# #     finally:
# #         conn.close()


# # # ✅ Signup Route
# # @app.post("/signup")
# # def signup(user: User):
# #     try:
# #         conn = get_db_connection()
# #         cursor = conn.cursor()
        
# #         # Check if user already exists
# #         cursor.execute("SELECT * FROM users WHERE email = %s OR username = %s", (user.email, user.username))
# #         if cursor.fetchone():
# #             conn.close()
# #             raise HTTPException(status_code=400, detail="User already exists!")

# #         # Hash the password
# #         hashed_password = pwd_context.hash(user.password)

# #         # Insert User
# #         cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
# #                        (user.username, user.email, hashed_password))
        
# #         conn.commit()
# #         conn.close()
# #         return {"status": "success", "message": "User registered successfully!"}

# #     except psycopg2.Error as e:
# #         logger.error(f"Database error: {e}")
# #         raise HTTPException(status_code=500, detail="Database error")
# #     except Exception as e:
# #         logger.error(f"Unexpected error: {e}")
# #         raise HTTPException(status_code=500, detail="Unexpected server error")


# # # ✅ Login Route
# # @app.post("/login")
# # def login(user: LoginRequest):
# #     try:
# #         conn = get_db_connection()
# #         cursor = conn.cursor()
        
# #         # Get user from database using email or username
# #         if user.email:
# #             cursor.execute("SELECT password FROM users WHERE email = %s", (user.email,))
# #         elif user.username:
# #             cursor.execute("SELECT password FROM users WHERE username = %s", (user.username,))
# #         else:
# #             raise HTTPException(status_code=400, detail="Email or username is required")
        
# #         result = cursor.fetchone()
        
# #         if result:
# #             stored_password = result[0]

# #             # Verify password
# #             if pwd_context.verify(user.password, stored_password):
# #                 return {"status": "success", "message": "Login successful"}
# #             else:
# #                 raise HTTPException(status_code=401, detail="Invalid credentials")
        
# #         raise HTTPException(status_code=401, detail="Invalid credentials")

# #     except psycopg2.Error as e:
# #         logger.error(f"Database error: {e}")
# #         raise HTTPException(status_code=500, detail="Database error")
# #     except Exception as e:
# #         logger.error(f"Unexpected error: {e}")
# #         raise HTTPException(status_code=500, detail="Unexpected server error")
    
# # # ✅ Add Book Route
# # @app.post("/books")
# # def add_book(book: Book):
# #     try:
# #         conn = get_db_connection()
# #         cursor = conn.cursor()
        
# #         cursor.execute("INSERT INTO books (title, author, year, genre, thumbnail, is_read) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
# #                        (book.title, book.author, book.year, book.genre, book.thumbnail, book.is_read))
        
# #         book_id = cursor.fetchone()[0]
# #         conn.commit()
# #         conn.close()
        
# #         return {"status": "success", "message": "Book added successfully!", "book_id": book_id}

# #     except psycopg2.Error as e:
# #         logger.error(f"Database error: {e}")
# #         raise HTTPException(status_code=500, detail="Database error")


# # # ✅ Update Book Route
# # @app.put("/books/{book_title}")
# # def update_book(book_title: str, book: UpdateBook):
# #     try:
# #         conn = get_db_connection()
# #         cursor = conn.cursor()
        
# #         # Check if book exists
# #         cursor.execute("SELECT id FROM books WHERE title = %s", (book_title,))
# #         if not cursor.fetchone():
# #             conn.close()
# #             raise HTTPException(status_code=404, detail="Book not found")

# #         # Update book details
# #         update_query = "UPDATE books SET "
# #         update_values = []
# #         if book.title:
# #             update_query += "title = %s, "
# #             update_values.append(book.title)
# #         if book.author:
# #             update_query += "author = %s, "
# #             update_values.append(book.author)
# #         if book.year:
# #             update_query += "year = %s, "
# #             update_values.append(book.year)
# #         if book.genre:
# #             update_query += "genre = %s, "
# #             update_values.append(book.genre)
# #         if book.thumbnail:
# #             update_query += "thumbnail = %s, "
# #             update_values.append(book.thumbnail)
# #         if book.is_read is not None:
# #             update_query += "is_read = %s, "
# #             update_values.append(book.is_read)

# #         # Remove trailing comma and add WHERE clause
# #         update_query = update_query.rstrip(", ") + " WHERE title = %s"
# #         update_values.append(book_title)

# #         cursor.execute(update_query, update_values)
# #         conn.commit()
# #         conn.close()
        
# #         return {"status": "success", "message": "Book updated successfully!"}

# #     except psycopg2.Error as e:
# #         logger.error(f"Database error: {e}")
# #         raise HTTPException(status_code=500, detail="Database error")


# # # ✅ Delete Book Route
# # @app.delete("/books/{book_title}")
# # def delete_book(book_title: str):
# #     try:
# #         conn = get_db_connection()
# #         cursor = conn.cursor()
        
# #         # Check if book exists
# #         cursor.execute("SELECT id FROM books WHERE title = %s", (book_title,))
# #         if not cursor.fetchone():
# #             conn.close()
# #             raise HTTPException(status_code=404, detail="Book not found")

# #         # Delete the book
# #         cursor.execute("DELETE FROM books WHERE title = %s", (book_title,))
# #         conn.commit()
# #         conn.close()
        
# #         return {"status": "success", "message": "Book deleted successfully!"}

# #     except psycopg2.Error as e:
# #         logger.error(f"Database error: {e}")
# #         raise HTTPException(status_code=500, detail="Database error")


# # # ✅ Fetch All Books Route
# # @app.get("/books", response_model=List[Book])
# # def get_books():
# #     try:
# #         conn = get_db_connection()
# #         cursor = conn.cursor()
        
# #         cursor.execute("SELECT title, author, year, genre, thumbnail, is_read FROM books")
# #         books = cursor.fetchall()
        
# #         conn.close()
        
# #         return [Book(title=row[0], author=row[1], year=row[2], genre=row[3], thumbnail=row[4], is_read=row[5]) for row in books]

# #     except psycopg2.Error as e:
# #         logger.error(f"Database error: {e}")
# #         raise HTTPException(status_code=500, detail="Database error")

# from fastapi import FastAPI, HTTPException, Depends
# from pydantic import BaseModel
# from typing import List, Optional
# import logging
# from passlib.context import CryptContext
# import base64
# from contextlib import contextmanager
# from database import Database
# import psycopg2

# # 🔧 Setup Logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # 🔐 Password Hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # 📌 FastAPI App
# app = FastAPI()

# # Database Dependency
# @contextmanager
# def get_db():
#     conn = None
#     try:
#         conn = Database.get_connection()
#         yield conn
#     except Exception as e:
#         logger.error(f"Database connection failed: {e}")
#         raise HTTPException(status_code=500, detail="Database connection failed")
#     finally:
#         if conn:
#             Database.return_connection(conn)

# # 📌 Schemas
# class User(BaseModel):
#     username: str
#     email: str
#     password: str

# class LoginRequest(BaseModel):
#     email: Optional[str] = None
#     username: Optional[str] = None
#     password: str

# class Book(BaseModel):
#     title: str
#     author: str
#     year: Optional[int] = None
#     genre: Optional[str] = None
#     thumbnail: Optional[bytes] = None
#     is_read: bool = False

#     class Config:
#         json_encoders = {
#             bytes: lambda v: base64.b64encode(v).decode('utf-8') if v else None
#         }

# class UpdateBook(BaseModel):
#     title: Optional[str] = None
#     author: Optional[str] = None
#     year: Optional[int] = None
#     genre: Optional[str] = None
#     thumbnail: Optional[str] = None
#     is_read: Optional[bool] = None

# class WishlistItem(BaseModel):
#     username: Optional[str] = None
#     email: Optional[str] = None
#     book_title: str

# # Health Check
# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}

# # ✅ 1. Signup Route
# @app.post("/signup")
# def signup(user: User, db = Depends(get_db)):
#     try:
#         with db.cursor() as cursor:
#             cursor.execute("SELECT id FROM users WHERE email = %s OR username = %s", 
#                          (user.email, user.username))
#             if cursor.fetchone():
#                 raise HTTPException(status_code=400, detail="User already exists")

#             hashed_password = pwd_context.hash(user.password)
#             cursor.execute(
#                 "INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id",
#                 (user.username, user.email, hashed_password)
#             )
#             return {"status": "success", "message": "User registered successfully!"}
#     except psycopg2.Error as e:
#         logger.error(f"Database error: {e}")
#         raise HTTPException(status_code=500, detail="Database operation failed")

# # ✅ 2. Login Route
# @app.post("/login")
# def login(user: LoginRequest, db = Depends(get_db)):
#     try:
#         with db.cursor() as cursor:
#             if user.email:
#                 cursor.execute("SELECT id, password FROM users WHERE email = %s", (user.email,))
#             elif user.username:
#                 cursor.execute("SELECT id, password FROM users WHERE username = %s", (user.username,))
#             else:
#                 raise HTTPException(status_code=400, detail="Email or username required")

#             result = cursor.fetchone()
#             if not result:
#                 raise HTTPException(status_code=401, detail="Invalid credentials")
            
#             if pwd_context.verify(user.password, result[1]):
#                 return {"status": "success", "message": "Login successful", "user_id": result[0]}
#             raise HTTPException(status_code=401, detail="Invalid credentials")
#     except psycopg2.Error as e:
#         logger.error(f"Database error: {e}")
#         raise HTTPException(status_code=500, detail="Database operation failed")

# # ✅ 3. Add Book Route
# @app.post("/books")
# def add_book(book: Book, db = Depends(get_db)):
#     try:
#         with db.cursor() as cursor:
#             cursor.execute(
#                 """INSERT INTO books (title, author, year, genre, thumbnail, is_read) 
#                 VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
#                 (book.title, book.author, book.year, book.genre, book.thumbnail, book.is_read)
#             )
#             book_id = cursor.fetchone()[0]
#             return {"status": "success", "message": "Book added", "book_id": book_id}
#     except psycopg2.Error as e:
#         logger.error(f"Database error: {e}")
#         raise HTTPException(status_code=500, detail="Database operation failed")

# # ✅ 4. Get All Books Route
# @app.get("/books", response_model=List[Book])
# def get_books(db = Depends(get_db)):
#     try:
#         with db.cursor() as cursor:
#             cursor.execute("SELECT title, author, year, genre, thumbnail, is_read FROM books")
#             books = cursor.fetchall()
#             return [Book(title=row[0], author=row[1], year=row[2], genre=row[3], thumbnail=row[4], is_read=row[5]) for row in books]
#     except psycopg2.Error as e:
#         logger.error(f"Database error: {e}")
#         raise HTTPException(status_code=500, detail="Database operation failed")

# # ✅ 5. Update Book Route
# @app.put("/books/{book_title}")
# def update_book(book_title: str, book: UpdateBook, db = Depends(get_db)):
#     try:
#         with db.cursor() as cursor:
#             # Build dynamic update query
#             updates = []
#             params = []
#             if book.title: updates.append("title = %s"); params.append(book.title)
#             if book.author: updates.append("author = %s"); params.append(book.author)
#             if book.year: updates.append("year = %s"); params.append(book.year)
#             if book.genre: updates.append("genre = %s"); params.append(book.genre)
#             if book.thumbnail: updates.append("thumbnail = %s"); params.append(book.thumbnail)
#             if book.is_read is not None: updates.append("is_read = %s"); params.append(book.is_read)
            
#             if not updates:
#                 raise HTTPException(status_code=400, detail="No fields to update")
            
#             query = f"UPDATE books SET {', '.join(updates)} WHERE title = %s"
#             params.append(book_title)
            
#             cursor.execute(query, params)
#             if cursor.rowcount == 0:
#                 raise HTTPException(status_code=404, detail="Book not found")
            
#             return {"status": "success", "message": "Book updated"}
#     except psycopg2.Error as e:
#         logger.error(f"Database error: {e}")
#         raise HTTPException(status_code=500, detail="Database operation failed")

# # ✅ 6. Delete Book Route
# @app.delete("/books/{book_title}")
# def delete_book(book_title: str, db = Depends(get_db)):
#     try:
#         with db.cursor() as cursor:
#             cursor.execute("DELETE FROM books WHERE title = %s", (book_title,))
#             if cursor.rowcount == 0:
#                 raise HTTPException(status_code=404, detail="Book not found")
#             return {"status": "success", "message": "Book deleted"}
#     except psycopg2.Error as e:
#         logger.error(f"Database error: {e}")
#         raise HTTPException(status_code=500, detail="Database operation failed")

# # ✅ 7. Wishlist Routes (Add and Get)
# @app.post("/wishlist")
# def add_to_wishlist(item: WishlistItem, db = Depends(get_db)):
#     try:
#         with db.cursor() as cursor:
#             # Verify book exists
#             cursor.execute("SELECT id FROM books WHERE title ILIKE %s", (item.book_title,))
#             book = cursor.fetchone()
#             if not book:
#                 raise HTTPException(status_code=404, detail="Book not found")

#             # Verify user exists
#             if item.username:
#                 cursor.execute("SELECT id FROM users WHERE username = %s", (item.username,))
#             elif item.email:
#                 cursor.execute("SELECT id FROM users WHERE email = %s", (item.email,))
#             else:
#                 raise HTTPException(status_code=400, detail="Username or email required")
            
#             user = cursor.fetchone()
#             if not user:
#                 raise HTTPException(status_code=404, detail="User not found")

#             # Add to wishlist
#             cursor.execute(
#                 "INSERT INTO wishlist (user_id, book_id) VALUES (%s, %s)",
#                 (user[0], book[0])
#             )
#             return {"status": "success", "message": "Added to wishlist"}
#     except psycopg2.Error as e:
#         logger.error(f"Database error: {e}")
#         raise HTTPException(status_code=500, detail="Database operation failed")

# @app.get("/wishlist/{user_id}")
# def get_wishlist(user_id: int, db = Depends(get_db)):
#     try:
#         with db.cursor() as cursor:
#             cursor.execute("""
#                 SELECT b.title, b.author, b.thumbnail 
#                 FROM wishlist w
#                 JOIN books b ON w.book_id = b.id
#                 WHERE w.user_id = %s
#             """, (user_id,))
#             return {"wishlist": cursor.fetchall()}
#     except psycopg2.Error as e:
#         logger.error(f"Database error: {e}")
#         raise HTTPException(status_code=500, detail="Database operation failed")

# # Startup Event
# @app.on_event("startup")
# async def startup():
#     try:
#         with get_db() as conn:
#             with conn.cursor() as cursor:
#                 cursor.execute("SELECT 1")
#         logger.info("✅ Database connection successful")
#     except Exception as e:
#         logger.error(f"❌ Database connection failed: {e}")
#         raise


# # ✅ Search Books Route
# @app.get("/books/search")
# def search_books(query: str):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
        
#         cursor.execute("SELECT title, author, year, genre, thumbnail, is_read FROM books WHERE title ILIKE %s OR author ILIKE %s", (f"%{query}%", f"%{query}%"))
#         books = cursor.fetchall()
        
#         conn.close()
        
#         return [Book(title=row[0], author=row[1], year=row[2], genre=row[3], thumbnail=row[4], is_read=row[5]) for row in books]

#     except psycopg2.Error as e:
#         logger.error(f"Database error: {e}")
#         raise HTTPException(status_code=500, detail="Database error")


# # ✅ Display Statistics Route
# @app.get("/stats")
# def get_stats():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
        
#         # Total books
#         cursor.execute("SELECT COUNT(*) FROM books")
#         total_books = cursor.fetchone()[0]
        
#         # Percentage read
#         cursor.execute("SELECT COUNT(*) FROM books WHERE is_read = TRUE")
#         read_books = cursor.fetchone()[0]
#         percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
        
#         conn.close()
        
#         return {
#             "status": "success",
#             "total_books": total_books,
#             "percentage_read": round(percentage_read, 2)
#         }

#     except psycopg2.Error as e:
#         logger.error(f"Database error: {e}")
#         raise HTTPException(status_code=500, detail="Database error")

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Response
from pydantic import BaseModel
from typing import List, Optional
import logging
from passlib.context import CryptContext
import base64
from contextlib import contextmanager
from database import Database
import psycopg2
import io
from PIL import Image

# 🔧 Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔐 Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 📌 FastAPI App
app = FastAPI()

# Database Dependency
@contextmanager
def get_db():
    conn = None
    try:
        conn = Database.get_connection()
        yield conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")
    finally:
        if conn:
            Database.return_connection(conn)

# 📌 Schemas
class User(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: str

class Book(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    genre: Optional[str] = None
    thumbnail: Optional[bytes] = None
    is_read: bool = False

    class Config:
        json_encoders = {
            bytes: lambda v: base64.b64encode(v).decode('utf-8') if v else None
        }

class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    thumbnail: Optional[str] = None
    is_read: Optional[bool] = None

class WishlistItem(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    book_title: str

class BookStats(BaseModel):
    total_books: int
    books_read: int
    books_unread: int
    percentage_read: float

# Health Check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# ✅ 1. Signup Route
@app.post("/signup")
def signup(user: User, db = Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE email = %s OR username = %s", 
                         (user.email, user.username))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="User already exists")

            hashed_password = pwd_context.hash(user.password)
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id",
                (user.username, user.email, hashed_password)
            )
            return {"status": "success", "message": "User registered successfully!"}
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")

# ✅ 2. Login Route
@app.post("/login")
def login(user: LoginRequest, db = Depends(get_db)):
    try:
        with db.cursor() as cursor:
            if user.email:
                cursor.execute("SELECT id, password FROM users WHERE email = %s", (user.email,))
            elif user.username:
                cursor.execute("SELECT id, password FROM users WHERE username = %s", (user.username,))
            else:
                raise HTTPException(status_code=400, detail="Email or username required")

            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
            if pwd_context.verify(user.password, result[1]):
                return {"status": "success", "message": "Login successful", "user_id": result[0]}
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")

# ✅ 3. Add Book Route (with file upload support)
@app.post("/books")
async def add_book(
    title: str,
    author: str,
    year: Optional[int] = None,
    genre: Optional[str] = None,
    is_read: bool = False,
    thumbnail: Optional[UploadFile] = File(None),
    db = Depends(get_db)
):
    try:
        thumbnail_data = None
        if thumbnail:
            # Read and validate image
            contents = await thumbnail.read()
            try:
                Image.open(io.BytesIO(contents))  # Validate image
                thumbnail_data = contents
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

        with db.cursor() as cursor:
            cursor.execute(
                """INSERT INTO books (title, author, year, genre, thumbnail, is_read) 
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
                (title, author, year, genre, thumbnail_data, is_read)
            )
            book_id = cursor.fetchone()[0]
            return {"status": "success", "message": "Book added", "book_id": book_id}
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")

# ✅ 4. Get All Books Route
@app.get("/books", response_model=List[Book])
def get_books(db = Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT title, author, year, genre, thumbnail, is_read FROM books")
            books = cursor.fetchall()
            return [Book(title=row[0], author=row[1], year=row[2], genre=row[3], thumbnail=row[4], is_read=row[5]) for row in books]
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")

# ✅ 5. Update Book Route
@app.put("/books/{book_title}")
def update_book(book_title: str, book: UpdateBook, db = Depends(get_db)):
    try:
        with db.cursor() as cursor:
            # Build dynamic update query
            updates = []
            params = []
            if book.title: updates.append("title = %s"); params.append(book.title)
            if book.author: updates.append("author = %s"); params.append(book.author)
            if book.year: updates.append("year = %s"); params.append(book.year)
            if book.genre: updates.append("genre = %s"); params.append(book.genre)
            if book.thumbnail: updates.append("thumbnail = %s"); params.append(book.thumbnail)
            if book.is_read is not None: updates.append("is_read = %s"); params.append(book.is_read)
            
            if not updates:
                raise HTTPException(status_code=400, detail="No fields to update")
            
            query = f"UPDATE books SET {', '.join(updates)} WHERE title = %s"
            params.append(book_title)
            
            cursor.execute(query, params)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Book not found")
            
            return {"status": "success", "message": "Book updated"}
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")

# ✅ 6. Delete Book Route
@app.delete("/books/{book_title}")
def delete_book(book_title: str, db = Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM books WHERE title = %s", (book_title,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Book not found")
            return {"status": "success", "message": "Book deleted"}
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")

# ✅ 7. Wishlist Routes
@app.post("/wishlist")
def add_to_wishlist(item: WishlistItem, db = Depends(get_db)):
    try:
        with db.cursor() as cursor:
            # Verify book exists
            cursor.execute("SELECT id FROM books WHERE title ILIKE %s", (item.book_title,))
            book = cursor.fetchone()
            if not book:
                raise HTTPException(status_code=404, detail="Book not found")

            # Verify user exists
            if item.username:
                cursor.execute("SELECT id FROM users WHERE username = %s", (item.username,))
            elif item.email:
                cursor.execute("SELECT id FROM users WHERE email = %s", (item.email,))
            else:
                raise HTTPException(status_code=400, detail="Username or email required")
            
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Add to wishlist
            cursor.execute(
                "INSERT INTO wishlist (user_id, book_id) VALUES (%s, %s)",
                (user[0], book[0])
            )
            return {"status": "success", "message": "Added to wishlist"}
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")

@app.get("/wishlist/{user_id}")
def get_wishlist(user_id: int, db = Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT b.title, b.author, b.thumbnail 
                FROM wishlist w
                JOIN books b ON w.book_id = b.id
                WHERE w.user_id = %s
            """, (user_id,))
            return {"wishlist": cursor.fetchall()}
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")

# ✅ 8. Search Books Route
@app.get("/books/search")
def search_books(query: str, db = Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT title, author, year, genre, thumbnail, is_read 
                FROM books 
                WHERE title ILIKE %s OR author ILIKE %s
            """, (f"%{query}%", f"%{query}%"))
            books = cursor.fetchall()
            return [Book(title=row[0], author=row[1], year=row[2], genre=row[3], thumbnail=row[4], is_read=row[5]) for row in books]
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")

# ✅ 9. Book Statistics Route
@app.get("/stats", response_model=BookStats)
def get_stats(db = Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM books")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM books WHERE is_read = TRUE")
            read = cursor.fetchone()[0]
            
            percentage = (read / total) * 100 if total > 0 else 0
            
            return BookStats(
                total_books=total,
                books_read=read,
                books_unread=total - read,
                percentage_read=round(percentage, 2)
            )
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")

# ✅ 10. Get Book Thumbnail Route
@app.get("/books/{book_id}/thumbnail")
def get_thumbnail(book_id: int, db = Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT thumbnail FROM books WHERE id = %s", (book_id,))
            result = cursor.fetchone()
            if not result or not result[0]:
                raise HTTPException(status_code=404, detail="Thumbnail not found")
            
            return Response(content=result[0], media_type="image/jpeg")
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")

# Startup Event
@app.on_event("startup")
async def startup():
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
        logger.info("✅ Database connection successful")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise