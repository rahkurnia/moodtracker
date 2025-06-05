import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime

DATA_FILE = 'data.json'

# Fungsi untuk membaca data dari file
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

# Fungsi untuk menyimpan data ke file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Tambah entri baru
def add_entry(date, story, mood):
    data = load_data()
    data.append({
        "date": date,
        "story": story,
        "mood": mood
    })
    save_data(data)

# Urutkan data berdasarkan tanggal
def sort_by_date(data):
    return sorted(data, key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"))

# Cari cerita yang mengandung keyword
def search_by_keyword(data, keyword):
    return [d for d in data if keyword.lower() in d['story'].lower()]

# Kelas utama aplikasi GUI
class MoodTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Tracker")

        self.frame = tk.Frame(root, bg="#fdf1d0", padx=30, pady=30)
        self.frame.pack()

        # Input tanggal
        tk.Label(self.frame, text="Tanggal berapa hari ini?", font=('Arial', 10)).pack()
        date_frame = tk.Frame(self.frame)
        date_frame.pack()

        self.day_entry = tk.Entry(date_frame, width=4)
        self.month_entry = tk.Entry(date_frame, width=4)
        self.year_entry = tk.Entry(date_frame, width=6)

        self.day_entry.pack(side=tk.LEFT)
        tk.Label(date_frame, text="/").pack(side=tk.LEFT)
        self.month_entry.pack(side=tk.LEFT)
        tk.Label(date_frame, text="/").pack(side=tk.LEFT)
        self.year_entry.pack(side=tk.LEFT)

        # Input cerita
        tk.Label(self.frame, text="Ada cerita apa hari ini?", font=('Arial', 10)).pack()
        self.story_entry = tk.Entry(self.frame)
        self.story_entry.pack()

        # Input mood
        tk.Label(self.frame, text="Bagaimana perasaanmu?", font=('Arial', 10)).pack()
        self.mood_var = tk.StringVar()
        mood_options = ["😌", "🙂", "😍", "😞", "😡"]
        mood_frame = tk.Frame(self.frame)
        mood_frame.pack()
        for mood in mood_options:
            tk.Radiobutton(mood_frame, text=mood, variable=self.mood_var, value=mood).pack(side=tk.LEFT)

        # Tombol Simpan & Riwayat
        button_frame = tk.Frame(self.frame, pady=10)
        button_frame.pack()
        tk.Button(button_frame, text="Riwayat", command=self.show_history).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Simpan", command=self.save_mood).pack(side=tk.LEFT)

    # Fungsi simpan data
    def save_mood(self):
        day = self.day_entry.get()
        month = self.month_entry.get()
        year = self.year_entry.get()
        story = self.story_entry.get()
        mood = self.mood_var.get()

        # Validasi input
        if not day or not month or not year or not story or not mood:
            messagebox.showerror("Error", "Semua kolom harus diisi.")
            return

        try:
            date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
        except:
            messagebox.showerror("Format salah", "Isi tanggal dengan benar (angka)")
            return

        add_entry(date, story, mood)
        messagebox.showinfo("Tersimpan", "Mood kamu sudah disimpan!")

        # Kosongkan input
        self.day_entry.delete(0, tk.END)
        self.month_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.story_entry.delete(0, tk.END)
        self.mood_var.set("")

    # Pilih tampilan riwayat: mingguan atau bulanan
    def show_history(self):
        def display(option):
            top.destroy()
            self.render_history(option)

        top = tk.Toplevel(self.root)
        top.title("Pilih Riwayat")
        tk.Label(top, text="Seperti apa kamu ingin riwayatmu ditampilkan?").pack(pady=10)
        tk.Button(top, text="Per minggu", command=lambda: display("week")).pack(pady=5)
        tk.Button(top, text="Per bulan", command=lambda: display("month")).pack(pady=5)
        tk.Button(top, text="Batal", command=top.destroy).pack(pady=5)

    # Tampilkan data mood dan cerita
    def render_history(self, mode):
        top = tk.Toplevel(self.root)
        top.title("Riwayat")

        text_area = tk.Text(top, wrap=tk.WORD, width=50, height=20)
        text_area.pack()

        data = sort_by_date(load_data())

        mood_count = {"😌":0, "🙂":0, "😍":0, "😞":0, "😡":0}
        stories = []

        # Ambil data terakhir 7 hari atau 30 hari
        if mode == "week":
            filtered = data[-7:]
        else:
            filtered = data[-30:]

        for entry in filtered:
            mood_count[entry['mood']] += 1
            stories.append(entry['story'])

        summary = "Ini adalah curhatan user.\n"
        if filtered:
            summary += f"Contoh cerita: {filtered[-1]['story']}\n"
        summary += "\nRekapan mood:\n"
        for mood, count in mood_count.items():
            summary += f"{mood} : {count} kali\n"

        summary += "\nKata-kata hari ini :\n"
        if stories:
            summary += f"{stories[-1]}\n"
        else:
            summary += "(Belum ada data)\n"

        text_area.insert(tk.END, summary)

        # Tombol cari keyword
        def cari():
            keyword = simpledialog.askstring("Cari Cerita", "Masukkan keyword:")
            if keyword:
                result = search_by_keyword(data, keyword)
                hasil = f"Hasil pencarian '{keyword}':\n"
                for r in result:
                    hasil += f"{r['date']} - {r['mood']} - {r['story']}\n"
                text_area.delete("1.0", tk.END)
                text_area.insert(tk.END, hasil)

        tk.Button(top, text="Cari Cerita", command=cari).pack(pady=5)

# Jalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x500")
    app = MoodTrackerApp(root)
    root.mainloop()
