from flask import Flask
from flask import request, jsonify
import sql_connector as sql

app = Flask(__name__)

commands = {}

app.teardown_appcontext(sql.close_connection)
        
@app.route('/feeder', methods=['GET'])
def get_feeder():
    try:
        conn = sql.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, type, time, time_hours, time_minutes FROM feeder_options")
        row = cursor.fetchall()
        cursor.close()
        
        print(row[1])
        feeder = []
        
        for i in range(0, len(row)):
            # Map tuple to dictionary
            feeder.append({
                "id": row[i][0],
                "name": row[i][1],
                "type": row[i][2],
                "time": str(row[i][3]) if row[i][3] else None,
                "time_hours": row[i][4],
                "time_minutes": row[i][5],
            })
        
        return jsonify(feeder), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Send command to feeder
@app.route('/send_command/<int:feeder_id>', methods=['GET', 'POST'])
def feed_now(feeder_id):
    commands[feeder_id] = {"action": "feed"}
    return jsonify({"status": "queued"})


# Pico asks for command
@app.route('/command/<int:feeder_id>', methods=['GET'])
def get_command(feeder_id):

    if feeder_id in commands:
        cmd = commands.pop(feeder_id)
        return jsonify(cmd), 200

    return jsonify({"action": "none"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')