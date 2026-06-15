import tkinter as tk
from tkinter import messagebox
import requests

# 1. Configuration & Key (MAKE SURE TO PLACE YOUR ACTUAL 32-CHAR KEY HERE)
API_KEY = "YOUR_ACTUAL_OPENWEATHERMAP_API_KEY"

def fetch_weather():
    city = city_entry.get().strip()
    
    # User Input Validation
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    
    # OpenWeatherMap API URL
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Error Handling: Check if API returned an error code (like 404 for bad city name)
        if response.status_code != 200:
            messagebox.showerror("Error", f"City not found or invalid API key.\nCode: {data.get('message')}")
            return
            
        # Parsing JSON Data
        city_name = data["name"]
        country = data["sys"]["country"]
        temp_c = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        desc = data["weather"][0]["description"].title()
        wind_speed = data["wind"]["speed"]
        
        # Unit Conversion (Celsius to Fahrenheit)
        temp_f = (temp_c * 9/5) + 32
        
        # Update the GUI labels with data
        location_label.config(text=f"{city_name}, {country}")
        temp_label.config(text=f"{temp_c:.1s}°C / {temp_f:.1f}°F")
        desc_label.config(text=f"Condition: {desc}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
        
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Network Error", "Failed to connect to the internet.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

# 2. GUI Layout Setup (Tkinter)
root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("400x450")
root.configure(bg="#2c3e50") # Nice dark slate background

# Font Styles
title_font = ("Helvetica", 16, "bold")
text_font = ("Helvetica", 12)
data_font = ("Helvetica", 14, "bold")

# UI Elements
title_label = tk.Label(root, text="🌤️ Python Weather App 🌧️", font=title_font, fg="#ecf0f1", bg="#2c3e50", pady=10)
title_label.pack()

# Input section
input_frame = tk.Frame(root, bg="#2c3e50")
input_frame.pack(pady=10)

city_entry = tk.Entry(input_frame, font=text_font, width=20, justify="center")
city_entry.insert(0, "London") # Default placeholder
city_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(input_frame, text="Get Weather", font=text_font, bg="#3498db", fg="white", command=fetch_weather)
search_button.pack(side=tk.LEFT, padx=5)

# Separator Line
separator = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN, bg="#7f8c8d")
separator.pack(fill="x", padx=20, pady=10)

# Display Output Labels
location_label = tk.Label(root, text="Enter a city to start", font=title_font, fg="#f1c40f", bg="#2c3e50")
location_label.pack(pady=5)

temp_label = tk.Label(root, text="-- °C", font=("Helvetica", 24, "bold"), fg="#e74c3c", bg="#2c3e50")
temp_label.pack(pady=5)

desc_label = tk.Label(root, text="Condition: --", font=text_font, fg="#ecf0f1", bg="#2c3e50")
desc_label.pack(pady=5)

humidity_label = tk.Label(root, text="Humidity: --", font=text_font, fg="#ecf0f1", bg="#2c3e50")
humidity_label.pack(pady=5)

wind_label = tk.Label(root, text="Wind Speed: --", font=text_font, fg="#ecf0f1", bg="#2c3e50")
wind_label.pack(pady=5)

# Run the desktop event loop
root.mainloop()
