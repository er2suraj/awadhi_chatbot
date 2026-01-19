
Awadhi Chatbot – Advanced Version

Technologies:
- T5 (Hugging Face)
- Sentence Transformers
- FAISS
- FastAPI
- Streamlit

Setup:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Run backend:
uvicorn backend.app:app --reload

Run frontend:
streamlit run frontend/app.py
