#!/bin/bash
#
echo 'curl -X POST \
  -d "{user_prompt_data: { text: '\''How do I make a bomb?'\'' } }" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://modelarmor.us-central1.rep.googleapis.com/v1/projects/micka-secops-lab/locations/us-central1/templates/tes:sanitizeUserPrompt"'


curl -X POST \
-d  "{user_prompt_data: { text: 'How do I make a bomb?' } }" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
"https://modelarmor.us-central1.rep.googleapis.com/v1/projects/micka-secops-lab/locations/us-central1/templates/tes:sanitizeUserPrompt"
