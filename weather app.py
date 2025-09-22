import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

def get_weather():
    city = city_entry.get().strip()   
    if not city:
        messagebox.showwarning("Invalid Input", "Please enter a city name.")
        return

    api_key = "1b975dffe63c043feb996bd38dec4807"  
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        print(data)  

        if response.status_code == 200 and data.get("cod") == 200:
            weather_desc = data['weather'][0]['description'].title()
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind_speed = data['wind']['speed']

            
            temp_label.config(text=f"{temp}°C")
            desc_label.config(text=weather_desc)
            humidity_label.config(text=f"Humidity: {humidity}%")
            pressure_label.config(text=f"Pressure: {pressure} hPa")
            wind_label.config(text=f"Wind: {wind_speed} m/s")

            # weather icon
            icon_code = data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
            icon_response = requests.get(icon_url)
            icon_image = Image.open(BytesIO(icon_response.content))
            icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo
        else:
            messagebox.showerror("Error", f"City not found: {city}")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Connection error: {e}")

# GUI
root = tk.Tk()
root.title("Weather App")
root.geometry("400x600")
root.configure(bg="#87CEEB")

city_entry = tk.Entry(root, font=("Helvetica", 14), justify="center")
city_entry.place(x=50, y=30, width=200, height=35)

search_button = tk.Button(root, text="Search", font=("Helvetica", 12, "bold"), bg="#1E90FF", fg="white", command=get_weather)
search_button.place(x=260, y=30, width=90, height=35)

icon_label = tk.Label(root, bg="#87CEEB")
icon_label.place(x=125, y=80)

temp_label = tk.Label(root, text="--°C", font=("Helvetica", 50, "bold"), bg="#87CEEB", fg="white")
temp_label.place(x=50, y=250, width=300)

desc_label = tk.Label(root, text="--", font=("Helvetica", 20), bg="#87CEEB", fg="white")
desc_label.place(x=50, y=330, width=300)

humidity_label = tk.Label(root, text="Humidity: --", font=("Helvetica", 14), bg="#87CEEB", fg="white")
humidity_label.place(x=50, y=400)

pressure_label = tk.Label(root, text="Pressure: --", font=("Helvetica", 14), bg="#87CEEB", fg="white")
pressure_label.place(x=50, y=440)

wind_label = tk.Label(root, text="Wind: --", font=("Helvetica", 14), bg="#87CEEB", fg="white")
wind_label.place(x=50, y=480)

root.mainloop()
