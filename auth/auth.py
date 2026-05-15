import bcrypt
import streamlit as st
from database.models import User
from database.database import SessionLocal

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(username, email, password):
    db = SessionLocal()
    try:
        if db.query(User).filter((User.username == username) | (User.email == email)).first():
            return False, "Username or email already exists."
        
        hashed = hash_password(password)
        new_user = User(username=username, email=email, hashed_password=hashed)
        db.add(new_user)
        db.commit()
        return True, "Registration successful. Please login."
    finally:
        db.close()

def login_user(username, password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user and verify_password(password, user.hashed_password):
            st.session_state['user_id'] = user.id
            st.session_state['username'] = user.username
            st.session_state['logged_in'] = True
            return True, "Login successful."
        return False, "Invalid username or password."
    finally:
        db.close()

def logout_user():
    for key in ['user_id', 'username', 'logged_in']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state['logged_in'] = False
