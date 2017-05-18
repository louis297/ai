#!/usr/bin/env python3

# Copyright 2015 Conchylicultor. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""
Main script. See README.md for more information

Use python 3
"""

from chatbot import chatbot
from flask import Flask, request
app = Flask(__name__)
app.debug = True


# if __name__ == "__main__":
chatbot = chatbot.Chatbot()
chatbot.main()


@app.route("/")
def hello():

    question = request.args.get('q')
    questionSeq = []  # Will be contain the question as seen by the encoder
    answer = chatbot.singlePredict(question, questionSeq)
    if not answer:
        return 'Warning: sentence too long, sorry. Maybe try a simpler sentence.'
    print('2123')
    return '{}\n'.format(chatbot.textData.sequence2str(answer, clean=True))

app.run()
