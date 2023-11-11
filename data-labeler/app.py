from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Get list of .mp4 files in the static directory
    mp4_files = [f for f in os.listdir('static') if f.endswith('.mp4')]
    return render_template('index.html', mp4_files=mp4_files)

@app.route('/mark_time', methods=['POST'])
def mark_time():
    data = request.json
    timestamp = data.get('timestamp')
    filename = data.get('filename')
    label = data.get('label')
    # Use the video filename to name the timestamp file
    if filename:
        timestamp_filename = f"{os.path.splitext(filename)[0]}.txt"
        with open(timestamp_filename, "a") as file:
            file.write(f"{label}: {timestamp}\n")
        print(f"Saved timestamp {timestamp} to {timestamp_filename}")
        return jsonify(success=True)
    else:
        return jsonify(success=False, error="No filename provided")


if __name__ == '__main__':
    app.run(debug=True)
