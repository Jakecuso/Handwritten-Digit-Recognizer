import tkinter as tk
import numpy as np
import cv2
import PIL.Image, PIL.ImageDraw
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

# Load trained model
model = load_model("digit_recognizer.keras")

# Initialize drawing canvas
class DigitDrawer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Handwritten Digit Recognizer")
        self.geometry("350x400")  # Adjust window size

        # Create drawing canvas
        self.canvas = tk.Canvas(self, width=280, height=280, bg="white")
        self.canvas.pack()

        # Create buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        self.predict_button = tk.Button(self.button_frame, text="Predict", command=self.make_prediction)
        self.predict_button.pack(side=tk.RIGHT)

        # Label to display prediction
        self.result_label = tk.Label(self, text="Draw a digit and press 'Predict'", font=("Arial", 14))
        self.result_label.pack()

        # Bind mouse events for drawing
        self.canvas.bind("<B1-Motion>", self.paint)

        # Create an image to store drawings
        self.image = PIL.Image.new("L", (280, 280), 255)
        self.draw = PIL.ImageDraw.Draw(self.image)

    def paint(self, event):
        """Draw on the canvas"""
        x1, y1, x2, y2 = (event.x - 10), (event.y - 10), (event.x + 10), (event.y + 10)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=10)
        self.draw.ellipse([x1, y1, x2, y2], fill="black")

    def clear_canvas(self):
        """Clear the drawing canvas"""
        self.canvas.delete("all")
        self.image = PIL.Image.new("L", (280, 280), 255)
        self.draw = PIL.ImageDraw.Draw(self.image)
        self.result_label.config(text="Draw a digit and press 'Predict'")

    def make_prediction(self):
        """Preprocess the drawing and predict the digit"""
        img = self.image.resize((28, 28))
        img = np.array(img)

        # Improved preprocessing
        img = cv2.GaussianBlur(img, (5, 5), 0)  # Reduce noise
        img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)[1]  # Make edges sharper
        img = cv2.bitwise_not(img)  # Invert colors
        img = img / 255.0  # Normalize
        img = img.reshape(1, 28, 28, 1)  # Reshape for CNN input

        # Make prediction
        prediction = model.predict(img)[0]  # Get probabilities
        top_3_indices = np.argsort(prediction)[-3:][::-1]  # Get top 3 predictions
        top_3_confidences = prediction[top_3_indices] * 100  # Convert to percentages

        # Format the prediction result
        result_text = "Top Predictions:\n"
        for i in range(3):
            result_text += f"{top_3_indices[i]}: {top_3_confidences[i]:.2f}%\n"

        # Update result label
        self.result_label.config(text=result_text)

# Run the application
if __name__ == "__main__":
    app = DigitDrawer()
    app.mainloop()