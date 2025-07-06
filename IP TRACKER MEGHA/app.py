import tkinter as tk
from tkinter import ttk, messagebox
from ip_tracker import fetch_ip_details
from database import initialize_db, store_data, fetch_all_data, delete_data, update_data
from graph_visualizer import generate_graph
import folium
import webbrowser
import os
from datetime import datetime
import json

# Initialize database
initialize_db()

# UI Constants
BTN_WIDTH = 14
BTN_HEIGHT = 2

def create_gradient_frame(root):
    canvas = tk.Canvas(root, width=1000, height=700, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    for i in range(0, 700):
        r = int(i / 700 * 255)
        color = f"#{0:02x}{int(31 + (r * 0.4)):02x}{int(63 + (r * 0.6)):02x}"
        canvas.create_rectangle(0, i, 1000, i+1, outline=color, fill=color)
    return canvas

class TraceIPApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TraceIP - Know the Unknown")
        self.geometry("1000x700")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (WelcomePage, MainPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(WelcomePage)

    def show_frame(self, page_class):
        self.frames[page_class].tkraise()

class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        canvas = create_gradient_frame(self)

        center_frame = tk.Frame(canvas, bg="#001f3f")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        heading_font = ("Segoe Script", 30, "bold")
        subheading_font = ("Lucida Calligraphy", 24)

        tk.Label(center_frame, text="Welcome to", font=heading_font, bg="#001f3f", fg="white").pack(pady=10)
        tk.Label(center_frame, text="TraceIP: Know the Unknown", font=subheading_font, bg="#001f3f", fg="#00ffff").pack(pady=10)

        start_btn = tk.Button(center_frame, text="🚀 Get Started", font=("Arial", 16, "bold"), width=22, height=2,
                              bg="#00bcd4", fg="white", activebackground="#0097a7",
                              command=lambda: controller.show_frame(MainPage))
        start_btn.pack(pady=30)
        self.add_hover(start_btn, "#00bcd4", "#0097a7")

    def add_hover(self, btn, color, hover_color):
        def on_enter(e): btn.config(bg=hover_color)
        def on_leave(e): btn.config(bg=color)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        canvas = create_gradient_frame(self)

        title = tk.Label(canvas, text="TraceIP", font=("Times New Roman", 28, "bold"), bg="#001f3f", fg="white")
        title.pack(pady=20)

        tk.Label(canvas, text="Enter IP Address:", font=("Times New Roman", 14), bg="#001f3f", fg="white").pack()
        self.ip_entry = tk.Entry(canvas, font=("Times New Roman", 14), width=40)
        self.ip_entry.pack(pady=10)

        tk.Button(canvas, text="🔍 Fetch Details", font=("Times New Roman", 12, "bold"), bg="#00bcd4", fg="white",
                  width=BTN_WIDTH, height=BTN_HEIGHT, command=self.fetch_details).pack(pady=10)

        self.result_text = tk.Text(canvas, height=10, width=95, font=("Times New Roman", 11), bg="white", wrap="word")
        self.result_text.pack(pady=20)

        btn_frame = tk.Frame(canvas, bg="#001f3f")
        btn_frame.pack()

        buttons = [
            ("💾 Store Data", "#4CAF50", self.store_current_data),
            ("📄 Show All Data", "#2196F3", self.show_all_data),
            ("❌ Delete Data", "#f44336", self.delete_data_prompt),
            ("✏️ Update Data", "#ff9800", self.update_data_prompt),
            ("📊 Visualize", "#9c27b0", generate_graph),
            ("🗺️ Show Map", "#607d8b", self.show_map),
        ]

        for idx, (text, color, cmd) in enumerate(buttons):
            btn = tk.Button(btn_frame, text=text, font=("Times New Roman", 10, "bold"), bg=color, fg="white",
                            width=BTN_WIDTH, height=BTN_HEIGHT, command=cmd)
            btn.grid(row=0, column=idx, padx=5, pady=5)
            self.add_hover(btn, color)

        back_btn = tk.Button(canvas, text="⬅️ Back to Welcome", font=("Times New Roman", 11, "bold"),
                             bg="#222", fg="white", width=20, height=2,
                             command=lambda: controller.show_frame(WelcomePage))
        back_btn.pack(pady=20)
        self.add_hover(back_btn, "#222", "#444")

    def add_hover(self, btn, color, hover_color=None):
        hover_color = hover_color if hover_color else "#333"
        def on_enter(e): btn.config(bg=hover_color)
        def on_leave(e): btn.config(bg=color)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def fetch_details(self):
        ip = self.ip_entry.get().strip()
        if not ip:
            messagebox.showerror("Error", "Please enter an IP address.")
            return
        raw = fetch_ip_details(ip)
        if raw:
            try:
                loc = raw.get("loc", "").split(",")
                latitude, longitude = float(loc[0]), float(loc[1])
            except:
                latitude = longitude = None
            structured = {
                "ip": raw.get("ip", ""),
                "city": raw.get("city", ""),
                "region": raw.get("region", ""),
                "country": raw.get("country", ""),
                "latitude": latitude,
                "longitude": longitude,
                "isp": raw.get("org", ""),
                "timezone": raw.get("timezone", "")
            }
            self.last_details = {"ip": ip, "details": structured}
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, json.dumps(structured, indent=4))
        else:
            self.result_text.insert(tk.END, "Failed to fetch details.\n")

    def store_current_data(self):
        if not hasattr(self, 'last_details') or not self.last_details:
            messagebox.showerror("Error", "No data to store. Fetch an IP first.")
            return
        store_data(self.last_details["ip"], json.dumps(self.last_details["details"], indent=4))
        messagebox.showinfo("Success", "Data stored successfully.")

    def show_all_data(self):
        records = fetch_all_data()
        self.result_text.delete("1.0", tk.END)
        for rec in records:
            self.result_text.insert(tk.END, f"ID: {rec[0]} | IP: {rec[1]}\nDetails:\n{rec[2]}\n\n")

    def delete_data_prompt(self):
        self._simple_prompt("Enter Record ID to Delete:", delete_data, "deleted")

    def update_data_prompt(self):
        record_id = self._simple_input("Enter Record ID to Update:")
        if record_id:
            new_details = self._simple_input("Enter New Details (JSON):")
            if new_details:
                update_data(int(record_id), new_details)
                messagebox.showinfo("Updated", f"Record {record_id} updated successfully.")

    def _simple_prompt(self, msg, func, label):
        record_id = self._simple_input(msg)
        if record_id:
            func(int(record_id))
            messagebox.showinfo(label.capitalize(), f"Record {record_id} {label} successfully.")

    def _simple_input(self, prompt_text):
        popup = tk.Toplevel(self)
        popup.title(prompt_text)
        popup.geometry("300x120")
        popup.configure(bg="white")
        tk.Label(popup, text=prompt_text, bg="white").pack(pady=5)
        entry = tk.Entry(popup)
        entry.pack(pady=5)
        result = {}

        def submit():
            result['value'] = entry.get()
            popup.destroy()

        tk.Button(popup, text="Submit", command=submit).pack(pady=5)
        self.wait_window(popup)
        return result.get('value')

    def show_map(self):
        if not hasattr(self, 'last_details') or not self.last_details:
            messagebox.showerror("Error", "Fetch an IP first to generate map.")
            return
        details = self.last_details['details']
        if details.get("latitude") and details.get("longitude"):
            map_obj = folium.Map(location=[details["latitude"], details["longitude"]], zoom_start=10)
            popup_info = f"IP: {details['ip']}\nCity: {details['city']}, {details['region']}, {details['country']}"
            folium.Marker([details["latitude"], details["longitude"]], popup=popup_info).add_to(map_obj)
            file_name = f"ip_map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            map_obj.save(file_name)
            webbrowser.open(f"file://{os.path.abspath(file_name)}")
        else:
            messagebox.showinfo("Info", "Location data not available for this IP.")

if __name__ == "__main__":
    app = TraceIPApp()
    app.mainloop()
