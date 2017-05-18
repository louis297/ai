from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from chatbot import chatbot

bot = chatbot.Chatbot()
bot.main()


def index(request):
    # bot = chatbot.Chatbot()
    # bot.main()
    question = request.GET.get('q')
    questionSeq = []
    answer = bot.singlePredict(question, questionSeq)
    if not answer:
        return 'Warning: sentence too long, sorry. Maybe try a simpler sentence.'

    return HttpResponse(bot.textData.sequence2str(answer, clean=True))
