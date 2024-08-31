import re
import streamlit as st
from collections import defaultdict

# Tokenize function to capture words correctly
def tokenize(text):
    # Capture all words by correcting the regex pattern
    return set(re.findall(r'\b\w+\b', text.lower()))

# Function to build the inverted index
def build_inverted_index(docs):
    index = defaultdict(set)
    for doc_id, text in docs.items():
        words = tokenize(text)
        for word in words:
            index[word].add(doc_id)
    return index

# Function to handle boolean retrieval
def boolean_retrieval(index, query):
    query = query.lower()
    tokens = re.findall(r'\b\w+\b', query)  # Corrected token extraction to capture words correctly

    result_docs = set(index.keys())  # Initialize with all document IDs

    # Handle "AND" logic
    if "and" in tokens:
        terms = query.split('and')
        result_docs = set(index.get(terms[0].strip(), set()))
        for term in terms[1:]:
            term = term.strip()
            result_docs = result_docs.intersection(index.get(term, set()))
    
    # Handle "OR" logic
    elif "or" in tokens:
        terms = query.split("or")
        result_docs = set()
        for term in terms:
            term = term.strip()
            result_docs = result_docs.union(index.get(term, set()))
    
    # Handle "NOT" logic
    elif 'not' in tokens:
        terms = query.split('not')
        if len(terms) == 2:
            included_term = terms[0].strip()
            term_to_exclude = terms[1].strip()
            result_docs = index.get(included_term, set()).difference(index.get(term_to_exclude, set()))
    
    # Handle simple search with no operators
    else:
        result_docs = set()
        for token in tokens:
            result_docs = result_docs.union(index.get(token, set()))
    
    return result_docs

# Streamlit App
st.title("Boolean Retrieval System")
uploaded_files = st.file_uploader("Browse files", type="txt", accept_multiple_files=True)
documents = {}

# Handle file uploads
if uploaded_files:
    for i, file in enumerate(uploaded_files):
        file_text = file.read().decode('utf-8')
        doc_id = f"doc{i+1}"
        documents[doc_id] = file_text

    inverted_index = build_inverted_index(documents)

    query = st.text_input("Enter a boolean query")

    # Handle search query
    if query:
        results = boolean_retrieval(inverted_index, query)
        st.subheader("Search Results")

        # Display results
        if results:
            st.write("DocId:")
            st.write(", ".join(results))
        else:
            st.write("No documents matched your query")