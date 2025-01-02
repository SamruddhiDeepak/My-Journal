import json
import datetime
from pathlib import Path
import streamlit as st

# Path to the JSON file for saving journal entries
journal_file = Path("journal_entries.json")

# Function to load journal entries and moods from the JSON file
def load_entries():
    if journal_file.exists():
        with open(journal_file, "r") as file:
            try:
                data = json.load(file)
                entries = {datetime.datetime.strptime(key, "%Y-%m-%d").date(): value for key, value in data.get("entries", {}).items()}
                moods = {datetime.datetime.strptime(key, "%Y-%m-%d").date(): value for key, value in data.get("moods", {}).items()}
                return entries, moods
            except json.JSONDecodeError:
                st.warning("The JSON file is corrupted, resetting entries.")
                save_entries({}, {})  
                return {}, {}
    else:
        return {}, {}

# Function to save journal entries and moods to the JSON file
def save_entries(entries, moods):
    entries_serializable = {entry_date.strftime("%Y-%m-%d"): value for entry_date, value in entries.items()}
    moods_serializable = {entry_date.strftime("%Y-%m-%d"): value for entry_date, value in moods.items()}

    data = {
        "entries": entries_serializable,
        "moods": moods_serializable
    }
    with open(journal_file, 'w') as file:
        json.dump(data, file, indent=4)

if 'entries' not in st.session_state or 'mood' not in st.session_state:
    st.session_state.entries, st.session_state.mood = load_entries()

# Customizing the page 
st.markdown("""
    <style>
        .reportview-container {
            background-color: #f2e3d5;
        }
        .stButton>button {
            background-color:;
            color: white;
            border-radius: 10px;
            font-size: 16px;
            padding: 10px;
            width: 200px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: ;
        }
        .stTextInput>div>input {
            border-radius: 10px;
            padding: 10px;
        }
        .stTextArea>div>textarea {
            border-radius: 10px;
            padding: 10px;
            font-family: 'Arial', sans-serif;
        }
        .stSelectbox>div>div>div>input {
            border-radius: 10px;
        }
        .stMarkdown {
            font-family: 'Arial', sans-serif;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🌸 My Journal 🌸")
st.subheader("Share your thoughts, track your mood, and revisit your memories!🌼")

tab = st.radio("What do you wanna do?", ["Today’s Reflections 🖊️", "Yesterday’s Thoughts 🍂"])

if tab == "Today’s Reflections 🖊️":
    date_selected = st.date_input("Tap a date to share your vibes 📅", value=None, key="calendar_date")

    # Check if there's already an entry for the selected date
    if date_selected in st.session_state.entries:
        st.write(f"### ✨ Journal Entry for {date_selected} ✨")
        st.write(st.session_state.entries[date_selected])
        if date_selected in st.session_state.mood:
            st.write(f"**Mood on:** {st.session_state.mood[date_selected]}")
        if st.button("✏️ Edit Entry"):
            st.session_state.is_editing = True  

        if 'is_editing' in st.session_state and st.session_state.is_editing:
            with st.form(key="edit_entry_form"):
                entry_text = st.text_area("Edit your journal entry", st.session_state.entries[date_selected])
                mood = st.selectbox("How are you feeling today?", ["😊 Happy", "😞 Sad", "😎 Cool", "😴 Tired", "🥳 Excited", "😬 Anxious", "🤔 Thoughtful", "😒 Annoyed"], index=["😊 Happy", "😞 Sad", "😎 Cool", "😴 Tired", "🥳 Excited", "😬 Anxious", "🤔 Thoughtful", "😒 Annoyed"].index(st.session_state.mood.get(date_selected, "😊 Happy")))
                submit_button = st.form_submit_button("💾 Save Changes")
                if submit_button:
                    st.session_state.entries[date_selected] = entry_text
                    st.session_state.mood[date_selected] = mood  
                    save_entries(st.session_state.entries, st.session_state.mood)  
                    st.session_state.is_editing = False 
                    st.success(f"Your journal entry for {date_selected} has been updated! 📝")
                
    else:
        mood = st.selectbox("How are you feeling today?", ["😊 Happy", "😞 Sad", "😎 Cool", "😴 Tired", "🥳 Excited", "😬 Anxious", "🤔 Thoughtful", "😒 Annoyed"])
        entry_text = st.text_area("Pause and reflect—write freely about your day. This is your space to unwind.✨")
        if st.button("💾 Save Entry"):
            st.session_state.entries[date_selected] = entry_text
            st.session_state.mood[date_selected] = mood  
            save_entries(st.session_state.entries, st.session_state.mood)  
            st.success(f"Your journal entry for {date_selected} has been saved! 📝")

elif tab == "Yesterday’s Thoughts 🍂":
    past_date = st.date_input("Pick a date to revisit your entry 📖✨", value=None)

    if past_date in st.session_state.entries:
        st.write(f"**Your journal entry:**")
        st.write(st.session_state.entries[past_date])

        if past_date in st.session_state.mood:
            st.write(f"**Mood:** {st.session_state.mood[past_date]}")
    else:
        st.write("No entry found for this date yet. Start writing today! 😊")
