import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import DateEntry  # Perlu instalasi: pip install tkcalendar
from PIL import Image, ImageTk    # Perlu instalasi: pip install pillow
import json
from datetime import datetime

DATA_FILE = 'data.json'
LOGO_PATH = 'logo_unesa.png'  # Simpan logo di satu folder dengan file ini


# Node untuk LinkedList
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Struktur data dinamis: LinkedList
class MoodLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    # Menambahkan node baru ke akhir list
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self.size += 1

    # Mengubah linked list ke list biasa
    def to_list(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

    # Bubble sort manual berdasarkan tanggal
    def sort_by_date(self):
        data_list = self.to_list()
        n = len(data_list)
        for i in range(n):
            for j in range(0, n-i-1):
                d1 = datetime.strptime(data_list[j]['date'], "%Y-%m-%d")
                d2 = datetime.strptime(data_list[j+1]['date'], "%Y-%m-%d")
                if d1 > d2:
                    data_list[j], data_list[j+1] = data_list[j+1], data_list[j]
        self.head = None
        self.size = 0
        for item in data_list:
            self.append(item)

    # Linear search berdasarkan keyword di cerita
    def search_by_keyword(self, keyword):
        results = MoodLinkedList()
        curr = self.head
        while curr:
            if keyword.lower() in curr.data['story'].lower():
                results.append(curr.data)
            curr = curr.next
        return results

# Membaca data dari file JSON ke linked list
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            mood_list = MoodLinkedList()
            for item in data:
                mood_list.append(item)
            return mood_list
    except:
        return MoodLinkedList()

# Menyimpan linked list ke file JSON
def save_data(mood_list):
    with open(DATA_FILE, 'w') as f:
        json.dump(mood_list.to_list(), f, indent=2)

# Menambahkan entri mood ke list dan simpan
def add_entry(date, story, mood):
    mood_list = load_data()
    mood_list.append({"date": date, "story": story, "mood": mood})
    save_data(mood_list)

# GUI utama
class MoodTrackerApp:
    def __init__(self, root):
        # Mengatur tampilan awal GUI
        self.root = root
        self.root.title("Mood Tracker")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)

        self.bg_color = "#fdf1d0"
        self.text_color = "#5a3e36"
        self.button_color = "#f0c38e"

        self.root.configure(bg=self.bg_color)

        self.frame = tk.Frame(root, bg=self.bg_color, padx=30, pady=30)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Tambahkan logo UNESA
        try:
            logo = Image.open(LOGO_PATH)
            logo = logo.resize((50, 50))
            self.logo_img = ImageTk.PhotoImage(logo)
            tk.Label(self.root, image=self.logo_img, bg=self.bg_color).place(relx=1.0, x=-60, y=10, anchor='ne')
        except:
            pass  # jika logo gagal dimuat, tidak masalah

        # Judul dan tujuan
        tk.Label(self.frame, text="Mood Tracker", font=('Arial', 20, 'bold'), bg=self.bg_color, fg=self.text_color).pack()
        tk.Label(self.frame, text="Aplikasi ini membantu pengguna memantau kondisi emosional mereka dari waktu ke waktu\n"
                                  "melalui pencatatan dan analisis sederhana dengan pendekatan yang lebih praktis dan efisien.",
                 font=('Arial', 10), bg=self.bg_color, fg=self.text_color, justify="center").pack(pady=5)

        # Input tanggal pakai calendar
        tk.Label(self.frame, text="Tanggal hari ini:", bg=self.bg_color, fg=self.text_color).pack()
        self.date_entry = DateEntry(self.frame, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
        self.date_entry.pack(pady=2)

        # Input cerita
        tk.Label(self.frame, text="Ada cerita apa hari ini?", bg=self.bg_color, fg=self.text_color).pack()
        self.story_entry = tk.Entry(self.frame, width=50)
        self.story_entry.pack()

        # Input mood
        tk.Label(self.frame, text="Bagaimana perasaanmu?", bg=self.bg_color, fg=self.text_color).pack(pady=(10,0))
        self.mood_var = tk.StringVar()
        self.mood_options = ["😄", "😩", "😐", "😢", "😡"]
        self.mood_descriptions = {
            "😄": "Senang",
            "😩": "Lelah",
            "😐": "Biasa saja",
            "😢": "Sedih",
            "😡": "Marah"
        }
        mood_frame = tk.Frame(self.frame, bg=self.bg_color)
        mood_frame.pack()
        for mood in self.mood_options:
            btn = tk.Radiobutton(mood_frame, text=f"{mood}\n{self.mood_descriptions[mood]}", variable=self.mood_var,
                                 value=mood, bg=self.bg_color, fg=self.text_color, font=('Arial', 10), indicatoron=0, width=12, height=2)
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Tombol
        button_frame = tk.Frame(self.frame, bg=self.bg_color)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Simpan", command=self.save_mood, bg=self.button_color).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Riwayat", command=self.show_history, bg=self.button_color).pack(side=tk.LEFT, padx=10)

    # Simpan data mood
    def save_mood(self):
        date = self.date_entry.get()
        story = self.story_entry.get()
        mood = self.mood_var.get()

        if not date or not story or not mood:
            messagebox.showerror("Error", "Semua kolom harus diisi.")
            return

        add_entry(date, story, mood)
        messagebox.showinfo("Tersimpan", "Mood kamu sudah disimpan!")
        self.story_entry.delete(0, tk.END)
        self.mood_var.set("")

    # Menampilkan riwayat data dan analisis mood
    def show_history(self):
        top = tk.Toplevel(self.root)
        top.title("Riwayat Mood")
        top.geometry("600x500")
        top.configure(bg=self.bg_color)

        try:
            logo = Image.open(LOGO_PATH)
            logo = logo.resize((40, 40))
            self.logo_img2 = ImageTk.PhotoImage(logo)
            tk.Label(top, image=self.logo_img2, bg=self.bg_color).place(relx=1.0, x=-50, y=10, anchor='ne')
        except:
            pass

        text_area = tk.Text(top, wrap=tk.WORD, width=70, height=25, bg="#fff9e6", fg=self.text_color)
        text_area.pack(pady=10, padx=10)

        mood_list = load_data()
        mood_list.sort_by_date()
        data = mood_list.to_list()

        mood_count = {m: 0 for m in self.mood_options}
        stories = []

        filtered = data[-30:] if len(data) >= 30 else data
        for entry in filtered:
            mood_count[entry['mood']] += 1
            stories.append(entry['story'])

        total = sum(mood_count.values())
        sorted_mood = sorted(mood_count.items(), key=lambda x: x[1], reverse=True)
        most_common = sorted_mood[0][0] if sorted_mood else ""

        summary = "=== Statistik Mood Bulanan ===\n\n"
        for mood, count in sorted_mood:
            percent = (count / total * 100) if total > 0 else 0
            summary += f"{mood} ({self.mood_descriptions[mood]}): {count} kali ({percent:.1f}%)\n"

        summary += f"\nRata-rata mood kamu: {most_common} ({self.mood_descriptions.get(most_common, '-')})\n"
        summary += f"\nMotivasi untukmu:\n{self.get_motivation(most_common)}\n"

        if filtered:
            last = filtered[-1]
            summary += f"\n=== Cerita Terakhir ===\n{last['date']} - {last['mood']}\n{last['story']}\n"

        text_area.insert(tk.END, summary)
        text_area.config(state=tk.DISABLED)

        # Tombol tambahan: Riwayat per minggu
        def show_weekly_history():
            weekly_window = tk.Toplevel(top)
            weekly_window.title("Riwayat Mood Mingguan")
            weekly_window.geometry("600x500")
            weekly_window.configure(bg=self.bg_color)

            text_weekly = tk.Text(weekly_window, wrap=tk.WORD, width=70, height=25, bg="#fff9e6", fg=self.text_color)
            text_weekly.pack(pady=10, padx=10)

            week_data = data[-7:] if len(data) >= 7 else data
            week_count = {m: 0 for m in self.mood_options}

            for entry in week_data:
                week_count[entry['mood']] += 1

            total_week = sum(week_count.values())
            sorted_week = sorted(week_count.items(), key=lambda x: x[1], reverse=True)
            common_week = sorted_week[0][0] if sorted_week else ""

            summary = "=== Statistik Mood Mingguan ===\n\n"
            for mood, count in sorted_week:
                percent = (count / total_week * 100) if total_week > 0 else 0
                summary += f"{mood} ({self.mood_descriptions[mood]}): {count} kali ({percent:.1f}%)\n"

            summary += f"\nRata-rata mood minggu ini: {common_week} ({self.mood_descriptions.get(common_week, '-')})\n"
            summary += f"\nMotivasi:\n{self.get_motivation(common_week)}\n"

            if week_data:
                last = week_data[-1]
                summary += f"\n=== Cerita Terakhir Minggu Ini ===\n{last['date']} - {last['mood']}\n{last['story']}\n"

            text_weekly.insert(tk.END, summary)
            text_weekly.config(state=tk.DISABLED)

        # Tombol riwayat mingguan
        tk.Button(top, text="Riwayat Mingguan", command=show_weekly_history, bg=self.button_color).pack(pady=5)

        tk.Button(top, text="Cari Cerita", command=lambda: self.search_story(mood_list), bg=self.button_color).pack(pady=5)

    # Memunculkan algoritma search (linear search)
    def search_story(self, mood_list):
        keyword = simpledialog.askstring("Cari Cerita", "Masukkan kata kunci:")
        if keyword:
            result_list = mood_list.search_by_keyword(keyword)
            result = result_list.to_list()
            hasil = f"Hasil pencarian '{keyword}':\n\n"
            for r in result:
                hasil += f"{r['date']} - {r['mood']}\n{r['story']}\n\n"
            if not result:
                hasil += "Tidak ditemukan."
            messagebox.showinfo("Hasil Pencarian", hasil)

    # Memberi motivasi sesuai mood terbanyak
    def get_motivation(self, mood):
        motivasi = {
             "😄": "Wah keren sekali, tetap bahagia ya! Senyummu itu menular, semoga harimu selalu cerah!",
             "😩": "Ingat, istirahat itu penting. Semoga kamu segera merasa lebih segar dan semangat lagi!",
             "😐": "Hari-hari biasa juga berarti kamu stabil, terus jalani dengan santai dan jangan lupa bahagia ya!",
             "😢": "Sedih itu hal biasa, jangan dipikirin terlalu berat. Istirahat dulu kalau perlu, nanti juga akan lewat kok.",
             "😡": "Tenang dulu, yuk coba tarik napas dalam-dalam. Jangan biarkan amarah menguasaimu, kamu kuat kok!"
        }
        return motivasi.get(mood, "Tetaplah menulis dan sadari perasaanmu setiap hari.")

# Menjalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = MoodTrackerApp(root)
    root.mainloop()