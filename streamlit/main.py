from multiapp import MultiApp
import Home, calculator

app = MultiApp()

# Add all your application here
app.add_app("Home", Home.app)
app.add_app("streamlit", calculator.app)
# app.add_app("Page 2", app.app("Page 2"))

# # The main app
app.run()