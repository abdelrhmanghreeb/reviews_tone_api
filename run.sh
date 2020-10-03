echo "Running service now..."
gunicorn3 -b "0.0.0.0:$api_gunicorn_port" -w "$api_gunicorn_workers" --threads "$api_gunicorn_threads" -t "$api_gunicorn_timeout" reviews_tone_api.api:app