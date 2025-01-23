import requests
from tkinter import *
from PIL import Image, ImageTk
import test

class User_location :

    def __init__(self, root):
        self.window = root
        self.window.geometry("500x500")
        self.window.title("Weather Detactor")
        self.window.config(bg="#81BFDA")
        Label(self.window, text="Enter Your Latitude and longitude", bg="#81BFDA", font=("Calibri", 18, "bold")).place(x=100, y=40)
        self.longitude = Entry(self.window,  bg="white", width=15, font=("Arial", 15, "bold"))
        self.longitude.place(x=70, y=150)
        self.label_long = Label(self.window, text="Longitude", bg="#81BFDA",font=("Arial", 12, "bold"))
        self.label_long.place(x=100, y=180)
        self.latitude = Entry(self.window, bg="white", width=15, font=("Arial", 15, "bold"))
        self.latitude.place(x=270, y=150)
        self.label_lat = Label(self.window, text="Latitude", bg="#81BFDA", font=("Arial", 12, "bold"))
        self.label_lat.place(x=310, y=180)

        Button(self.window,
               text="Go Ahead",
               bg="blue",
               font=("Calibri", 18, "bold"),
               activebackground="blue",

               command=self.go_ahead).place(x=200, y=250)
        self.window.mainloop()


    def go_ahead(self):
        message = Label(self.window, text="", bg="#81BFDA")
        message.place(x=190, y=300)
        if not self.longitude.get() :
            self.label_long.config(fg="red")
        else :
            self.label_long.config(fg="black")

        if not self.latitude.get() :
            self.label_lat.config(fg="red")
        else :
            self.label_lat.config(fg="black")

        try:

            longitude = float(self.longitude.get())
            latitude = float(self.latitude.get())
            # get you api key from www.api.weather.com
            if longitude and latitude :
                parameter = {
                    "key": "Get Your Own key", 
                    "q": f"{longitude}, {latitude}"
                }

                response = requests.get(url="http://api.weatherapi.com/v1/current.json", params=parameter)

                if response.status_code == 200 :
                    self.window.destroy()
                    WeatherDetails(response.json())



                else :
                    message.config(text=response.json()['error']['message'])

        except ValueError :
            message.config(text="Incorrect latitude or longitude")


class WeatherDetails:
    def __init__(self, weather_data):
        self.weather_data = weather_data
        self.window = Tk()
        self.window.title("Weather Info")
        self.window.geometry("500x500")
        self.canvas = Canvas(self.window, height=500, width=500)
        self.canvas.pack()

        # Extract weather data
        self.location = self.weather_data['location']
        self.current = self.weather_data['current']
        # Load and resize images
        self.day_image = Image.open("day_image.jpg").resize((500, 500))
        self.day = ImageTk.PhotoImage(self.day_image)

        self.night_image = Image.open("night_image.jpg").resize((500, 500))
        self.night = ImageTk.PhotoImage(self.night_image)

        # Check whether it's day or night and set the background
        self.check_day_or_night()

        self.window.mainloop()

        # Ensure images are properly closed
        self.day_image.close()
        self.night_image.close()

    def check_day_or_night(self):
        day = self.current['is_day']
        print(self.weather_data)


        # Set the background image based on day or night
        if day == 1:
            print("Daytime")
            self.canvas.create_image(250, 250, image=self.day)
            self.all_labels("black")
        else:
            print("Nighttime")
            self.canvas.create_image(250,250, image=self.night)
            self.all_labels("white")


    def all_labels(self, foreground):
        name = self.location['name']
        region = self.location['region']
        country = self.location['country']

        self.canvas.create_text(350, 40, text=f"{name},{region},{country}", fill=foreground, font=("Consola", 14, "bold"),width=170)
        self.canvas.create_text(90, 80, text=f"{self.current["temp_c"]}°C", fill=foreground, font=("Consola", 39, "bold"))
        self.canvas.create_text(350, 130, text=f"wind speed : {self.current['wind_kph']}km",fill=foreground, font=("Consola", 14, "bold"))
        self.canvas.create_text(90, 340, text=f"Humidity : {self.current["humidity"]}%",fill=foreground, font=("Consola", 14, "bold"))
        self.canvas.create_text(90, 400, text=f"Heat Index : {self.current["heatindex_c"]}°C",fill=foreground, font=("Consola", 14, "bold"))
        self.canvas.create_text(390, 340, text=f"UV Rays : {self.current["uv"]}",fill=foreground, font=("Consola", 14, "bold"))
        self.canvas.create_text(390, 400, text=f"Dew Point : {self.current["dewpoint_c"]}°C",fill=foreground, font=("Consola", 14, "bold"))
        Button(self.window, text="Go Back", command=self.go_back, bg="#81BFDA", font=("Times New Roman", 18)).place(x=200, y=430)

    def go_back(self):
        self.window.destroy()
        window = Tk()
        app = User_location(window)








if __name__ == "__main__":
    root = Tk()
    app = User_location(root)

