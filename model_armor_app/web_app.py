from flask import Flask, render_template, request, jsonify
#import requests
from google.cloud import modelarmor_v1

client = modelarmor_v1.ModelArmorClient(transport="rest", client_options = {"api_endpoint" : "modelarmor.us-central1.rep.googleapis.com"})
PROJECT_ID = "micka-secops-lab" 
LOCATION = "us-central1" 
TEMPLATE_ID = "tes"
app = Flask(__name__)

# def match_enum_to_string(match_enum):
#     if match_enum == 1:

#     return match_str

def match_enum_to_string(match_enum):
    if match_enum == 2:
        match_str = "MATCH_FOUND"
    else: 
        match_str = "NO_MATCH_FOUND"
    return match_str

def get_general_verdict(response):
    return match_enum_to_string(response.sanitization_result.filter_match_state)

def get_sdp_verdict(response):
    match_enum = response.sanitization_result.filter_results["sdp"].sdp_filter_result.inspect_result.match_state
    return match_enum_to_string(match_enum)

def get_pi_and_jailbreak_verdict(response):
    match_enum = response.sanitization_result.filter_results["pi_and_jailbreak"].pi_and_jailbreak_filter_result.match_state
    print(match_enum)
    return match_enum_to_string(match_enum)

def get_malicious_uris_verdict(response):
    match_enum = response.sanitization_result.filter_results["malicious_uris"].malicious_uri_filter_result.match_state
    return match_enum_to_string(match_enum)

def get_csam_verdict(response):
    match_enum = response.sanitization_result.filter_results["csam"].csam_filter_filter_result.match_state
    return match_enum_to_string(match_enum)

def get_sexually_explicit_verdict(response):
    match_enum = response.sanitization_result.filter_results["rai"].rai_filter_result.rai_filter_type_results["sexually_explicit"].match_state
    return match_enum_to_string(match_enum)

def get_hate_speech_verdict(response):
    match_enum = response.sanitization_result.filter_results["rai"].rai_filter_result.rai_filter_type_results["hate_speech"].match_state
    print(match_enum)
    return match_enum_to_string(match_enum)

def get_harassment_verdict(response):
    match_enum = response.sanitization_result.filter_results["rai"].rai_filter_result.rai_filter_type_results["harassment"].match_state
    return match_enum_to_string(match_enum)

def get_dangerous_verdict(response):
    match_enum = response.sanitization_result.filter_results["rai"].rai_filter_result.rai_filter_type_results["dangerous"].match_state
    return match_enum_to_string(match_enum)





@app.route('/', methods=['GET', 'POST'])
def index():
    general_verdict = "None"
    user_input = "None"
    sdp_verdict = "None"
    pi_and_jailbreak = "None"
    malicious_uris = "None"
    csam = "None"
    sexually_explicit = "None"
    hate_speech = "None"
    harassment = "None"
    dangerous = "None"

    if request.method == 'POST':  
        user_input = request.form['user_input']
        # Initialize request argument(s)
        user_prompt_data = modelarmor_v1.DataItem()
        user_prompt_data.text = user_input
        model_armor_request = modelarmor_v1.SanitizeUserPromptRequest(
            name=f"projects/{PROJECT_ID}/locations/{LOCATION}/templates/{TEMPLATE_ID}",
            user_prompt_data=user_prompt_data,
        )

        response = client.sanitize_user_prompt(request=model_armor_request)
        print("User Input: " + user_input)
        print(response)
        general_verdict = get_general_verdict(response)
        sdp_verdict = get_sdp_verdict(response)
        pi_and_jailbreak = get_pi_and_jailbreak_verdict(response)
        malicious_uris = get_malicious_uris_verdict(response)
        csam = get_csam_verdict(response)
        sexually_explicit = get_sexually_explicit_verdict(response)
        hate_speech =  get_hate_speech_verdict(response)
        harassment = get_harassment_verdict(response)
        dangerous = get_dangerous_verdict(response)
    categories = {
        "General Verdict": general_verdict,
        "Security Data Prevention": sdp_verdict,
        "Prompt Injection and Jailbreak": pi_and_jailbreak,
        "Malicious URIs": malicious_uris,
        "CSAM": csam,
        "Sexually Explicit": sexually_explicit,
        "Hate Speech": hate_speech,
        "Harassment": harassment,
        "Dangerous": dangerous
    }

    return render_template(
        'index.html', 
        user_input = user_input,
        categories = categories
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

