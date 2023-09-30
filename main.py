from flask import Flask, request, redirect, render_template
import random
import string

app = Flask(__name__)
url_mapping = {}
domain_mapping = {}


def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


def get_domain(url):
    return url.split("//")[1].split("/")[0]


def is_short_url_unique(short_url):
    return short_url not in url_mapping


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    
    domain = get_domain(long_url)
    if domain in domain_mapping:
        short_url = domain_mapping[domain]
    else:
        short_url = generate_short_url()
        domain_mapping[domain] = short_url
    
    while not is_short_url_unique(short_url):
        short_url = generate_short_url()
    
    url_mapping[short_url] = long_url
    
    return render_template('shortened.html', short_url=short_url)


@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    if short_url in url_mapping:
        long_url = url_mapping[short_url]
        return redirect(long_url)
    else:
        return "URL not found", 404


if __name__ == '__main__':
    app.run(debug=True)
