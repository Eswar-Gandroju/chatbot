                          Technical Documentation: Flask Chatbot with Product Search & Authentication


    1. Project Overview
          .This project is a web-based chatbot application built with Flask that allows users to:

          .Sign up, log in, and log out securely.

          .Chat with a bot that can search a product inventory.

          .Search products by keyword, price, rating filters.

          .View chat history for the last 7 days.

          .Store user chats and product data in SQLite.

   2. Architecture
       Components:
             Frontend: HTML templates (login.html, signup.html, chatbot.html) rendered by Flask for user interface.

             Backend: Flask app managing user sessions, authentication, routing, and API endpoints.

             Database: SQLite DB (db/products.db) to persist users, chat logs, and product data.

             Blueprint: Modular Flask blueprint (chatbot_bp) to handle chatbot API routes.

      Flow:
             User visits site → logs in or signs up.

             Upon login, user accesses chatbot interface.

             User sends chat messages to /api/chat.

             Chatbot processes message, queries products table if needed, returns response.

             Chat logs stored in chat_logs table.

            User can query chat history for last 7 days.

            Users stored with hashed passwords in users table.

            Product inventory prepopulated with mock data.


   3. Choice of Tools / Frameworks:

       Tool/Framework Purpose :
            Flask	Lightweight Python web framework for backend API and routing.

            SQLite	Lightweight embedded relational DB for easy data persistence, no server needed.

            Werkzeug Security	For secure password hashing and verification.

            HTML/CSS	Frontend templates for user interface.

            Python sqlite3	Native Python library for SQLite DB interaction.

            Blueprint (Flask)	Organizing routes modularly for chatbot APIs.

            Random / OS libraries	For mock data generation and folder management.

   4. Database Schema
        Tables:
         
              users :

                  id (INTEGER PRIMARY KEY AUTOINCREMENT)

                  username (TEXT UNIQUE NOT NULL)

                  password (TEXT NOT NULL, hashed)

             chat_logs :

                  id (INTEGER PRIMARY KEY AUTOINCREMENT)

                  username (TEXT)

                  message (TEXT)

                  sender (TEXT — either 'user' or 'bot')

                  timestamp (DATETIME DEFAULT CURRENT_TIMESTAMP)

             products :

                  product_id (INTEGER PRIMARY KEY AUTOINCREMENT)
 
                  name (TEXT)

                  category (TEXT)

                  brand (TEXT)

                  price (INTEGER)

                  rating (REAL)

                  stock (INTEGER)
 
                  description (TEXT)

                  image_url (TEXT)


   5. Mock Data Creation

            The generate_inventory.py script:

            Creates all tables if not exist.

            Inserts 100 mock product records with random categories, brands, prices, ratings, and stock.

            Uses dummy image URLs for product thumbnails.

            Descriptions mapped per category.

            User and chat log tables are empty initially.



  6. Key Functionalities

       6.1 User Authentication
        
           Sign up: Validates username uniqueness, strong password (regex), and confirms password match.

           Login: Verifies username/password via hashed password check.

           Session: Uses Flask session for login state.

           Logout: Clears session.


      6.2 Chatbot API

           /api/chat POST endpoint:

           Accepts JSON with message and username.

           Parses user message for keywords: "show", "find", "search".

           Extracts filters like max price ("under 50000") and minimum rating ("rating above 4").

           Queries products and responds with number of matched products.

           Logs both user and bot messages.

           /api/products GET endpoint:

           Supports query params: keyword, max_price, min_rating.

           Returns filtered product list.

           /api/history GET endpoint:

           Returns last 7 days chat logs of a user.


   7. Potential Challenges & Solutions

           Challenge	How Handled / Recommended Solution

           Password security	Used werkzeug.security to hash passwords securely before storage.

           SQL Injection risk	Used parameterized queries (? placeholders) to avoid injection.
            
           Database locking	Used context managers (with sqlite3.connect() as conn:) for safe DB access.

           Handling concurrent requests	SQLite is limited in concurrency; avoid heavy write loads or consider PostgreSQL if scaling.

           User session security	Flask session secret key is set; consider HTTPS in production.

           Parsing natural language input	Basic keyword and phrase detection implemented; could be improved with NLP libraries (spaCy,  NLTK).

           Scalability of chatbot logic	Current logic is simple; for complex bots, integrate ML/NLP or external services.

           Data consistency & integrity	Schema constraints applied (e.g., UNIQUE username), handle DB exceptions gracefully.


    8. Future Enhancements

           Add pagination for product search results.

           Improve chatbot understanding using NLP.

           Add password reset functionality.

           Store user profile data (email, preferences).
 
           Add product images in frontend UI.
 
           Switch from SQLite to a more scalable DB in production.

           Add user roles (admin, customer).

           Deploy with HTTPS and Docker containers.