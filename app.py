from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        url = request.form['url']
        content = scrape_website(url)
        test_cases = generate_test_cases(content)
        return render_template('index.html', test_cases=test_cases)
    return render_template('index.html')

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract the main content or specific elements
    content = soup.get_text()
    return content

def generate_test_cases(content):
    modelNme = HfApiModel(token="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")
    agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=modelNme)
    prompt = f"Generate test cases based on the following content:\n{content}"
    test_cases = agent.run(prompt)
    return test_cases

    # agent = Agent("You are a helpful AI that generates software test cases.")
    # prompt = f"Generate test cases based on the following content:\n{content}"
    # test_cases = agent.run(prompt)
    # return test_cases

# def agentCall(content):
#     modelNme = HfApiModel(token="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")
#     agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=modelNme)
#     print(content)
#     agent.run(content, "Analyse this content and write test cases")


if __name__ == '__main__':
    app.run(debug=True)