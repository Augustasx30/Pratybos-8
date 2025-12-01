import azure.functions as func
import logging
import os
import google.generativeai as genai

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="AskGoogleAI")
def AskGoogleAI(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Gauta užklausa į Google Gemini fasadą.')

    question = req.params.get('question')
    if not question:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            question = req_body.get('question')

    if not question:
        return func.HttpResponse(
            "Klaida: Nenurodytas klausimas. Naudokite parametrą 'question'.",
            status_code=400
        )

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return func.HttpResponse(
            "Serverio klaida: Nerastas GOOGLE_API_KEY nustatymo.",
            status_code=500
        )

    try:
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        response = model.generate_content(question)
        
        return func.HttpResponse(response.text, status_code=200)

    except Exception as e:
        logging.error(f"Google AI klaida: {e}")
        return func.HttpResponse(f"Įvyko klaida: {str(e)}", status_code=500)