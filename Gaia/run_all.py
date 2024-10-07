import subprocess

# Start Flask
flask_process = subprocess.Popen(["flask", "run", "--host=0.0.0.0", "--port=5000"], cwd=r"C:\Users\NOSfe\Desktop\Capstone\GaiaCapstone\Gaia\app")

# Start Rasa action server
actions_process = subprocess.Popen(["rasa", "run", "actions"], cwd=r"C:\Users\NOSfe\Desktop\Capstone\GaiaCapstone\Gaia\app\actions")

# # Add a small delay to ensure the action server starts before the Rasa server
# actions_process.wait(timeout=5)

# Start Rasa server
rasa_process = subprocess.Popen(["rasa", "run", "--enable-api", "--cors", "*", "-m", "models"], cwd=r"C:\Users\NOSfe\Desktop\Capstone\GaiaCapstone\Gaia\app")

# Wait for all processes to complete
flask_process.wait()
actions_process.wait()
rasa_process.wait()