from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import FAQ

def get_chatbot_response(user_query, similarity_threshold=0.25):
    if len(user_query.strip()) < 3:
        return "I'm sorry, could you please provide a more specific question?"
        
    faqs = list(FAQ.objects.all())
    
    if not faqs:
        return "Sorry, I don't have that information yet."

    questions = [faq.question for faq in faqs]
    
    # Add the user query to the list so its vocabulary is included in the TF-IDF matrix
    questions.append(user_query)
    
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(questions)
        vectors = tfidf_matrix.toarray()
    except ValueError:
        # Happens if vocab is empty or simple text is skipped
        return "Sorry, I don't have that information yet."
    
    user_vector = vectors[-1]
    question_vectors = vectors[:-1]
    
    cosine_similarities = cosine_similarity([user_vector], question_vectors).flatten()
    
    if len(cosine_similarities) == 0:
        return "Sorry, I don't have that information yet."

    highest_similarity_index = cosine_similarities.argmax()
    highest_similarity_score = cosine_similarities[highest_similarity_index]
    
    if highest_similarity_score >= similarity_threshold:
        return faqs[highest_similarity_index].answer
    else:
        return "I'm not quite sure I understand. Could you rephrase your question or try one of the suggestions above?"
