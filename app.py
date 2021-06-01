# importing required modules
from ss import app
from dotenv import load_dotenv
load_dotenv()
# importing required modules end

# running the app
if __name__ == '__main__':

    app.run(debug=True, port=8000)
# running the app end
