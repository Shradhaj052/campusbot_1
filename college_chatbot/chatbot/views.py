from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.http import JsonResponse
from .models import FAQ,ChatHistory
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect


@login_required
def chatbot_ui(request):
    return render(request, "chatbot/index.html")

@login_required(login_url="/")
def chatbot_ui(request):
    return render(request, "chatbot/index.html")

def chat_response(request):
    user_msg = request.GET.get("message")

    faqs = FAQ.objects.all()
    questions = [faq.question.lower() for faq in faqs]
    answers = [faq.answer for faq in faqs]

    if not questions:
        return JsonResponse({"reply": "No FAQ data found."})

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(questions + [user_msg.lower()])

    similarity = cosine_similarity(vectors[-1], vectors[:-1])

    best_match = similarity.argmax()
    best_score = similarity[0][best_match]

    print("Similarity score:", best_score) # for debugging

    if best_score > 0.15:
        reply = answers[best_match]
    else:
        reply = "Sorry, I couldn't understand your question."

    ChatHistory.objects.create(
        user=request.user,
        user_message=user_msg,
        bot_reply=reply
    )

    return JsonResponse({"reply": reply})

def analytics(request):
    total_chats = ChatHistory.objects.count()
    top_questions = ChatHistory.objects.values("user_message").annotate(count=Count("user_message")).order_by("-count")[:5]

    return render(request, "chatbot/analytics.html", {
        "total": total_chats,
        "top": top_questions
    })
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "chatbot/signup.html", {"form": form})