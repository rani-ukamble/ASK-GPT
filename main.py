from flask import Flask, request, render_template
import google.generativeai as genai

app = Flask(__name__)

# Configure the API key
genai.configure(api_key="")

# Define the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

@app.route("/", methods=["GET", "POST"])
def index():
    response_html = ""
    if request.method == "POST":
        prompt = request.form.get("prompt")
        if prompt:
            try:
                # Start a chat session
                chat_session = model.start_chat(history=[])
                # Send the prompt to the model and get the response
                response = chat_session.send_message(prompt)
                response_text = response.text

                # Process the response to format it
                response_html = process_response(response_text)
            except Exception as e:
                response_html = f"<p>Error: {str(e)}</p>"
        else:
            response_html = "<p>No prompt provided.</p>"
    
    return render_template("gemini.html", response=response_html)

def process_response(text):
    # Split the text into paragraphs based on double newlines
    paragraphs = text.split('\n\n')

    # Create numbered paragraphs
    numbered_paragraphs = ''
    for i, para in enumerate(paragraphs):
        para = para.strip()
        if para:
            # Replace newlines within paragraphs with <br> for line breaks
            para = para.replace('\n', '<br>')
            numbered_paragraphs += f"<p>{i + 1}. {para}</p>"

    return numbered_paragraphs

if __name__ == "__main__":
    app.run(debug=True)
