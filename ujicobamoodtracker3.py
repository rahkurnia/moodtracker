import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime

DATA_FILE = 'data.json'

# Node untuk LinkedList
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# LinkedList untuk menyimpan data mood
class MoodLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def sort_by_date(self):
        # Convert to list for sorting
        data_list = self.to_list()
        # Bubble sort based on date
        n = len(data_list)
        for i in range(n):
            for j in range(0, n-i-1):
                date1 = datetime.strptime(data_list[j]['date'], "%Y-%m-%d")
                date2 = datetime.strptime(data_list[j+1]['date'], "%Y-%m-%d")
                if date1 > date2:
                    data_list[j], data_list[j+1] = data_list[j+1], data_list[j]
        
        # Rebuild the linked list
        self.head = None
        self.size = 0
        for item in data_list:
            self.append(item)
    
    def search_by_keyword(self, keyword):
        results = MoodLinkedList()
        current = self.head
        while current:
            if keyword.lower() in current.data['story'].lower():
                results.append(current.data)
            current = current.next
        return results

# Fungsi untuk membaca data dari file
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

# Fungsi untuk menyimpan data ke file
def save_data(mood_list):
    with open(DATA_FILE, 'w') as f:
        json.dump(mood_list.to_list(), f, indent=2)

# Tambah entri baru
def add_entry(date, story, mood):
    mood_list = load_data()
    mood_list.append({
        "date": date,
        "story": story,
        "mood": mood
    })
    save_data(mood_list)

# Kelas utama aplikasi GUI
class MoodTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Tracker")
        
        # Warna tema
        self.bg_color = "#fdf1d0"
        self.button_color = "#f0c38e"
        self.text_color = "#5a3e36"
        
        self.root.configure(bg=self.bg_color)
        
        self.frame = tk.Frame(root, bg=self.bg_color, padx=30, pady=30)
        self.frame.pack()

        # Judul aplikasi
        tk.Label(self.frame, text="Mood Tracker", font=('Arial', 16, 'bold'), 
                bg=self.bg_color, fg=self.text_color).pack(pady=10)

        # Input tanggal
        tk.Label(self.frame, text="Tanggal berapa hari ini?", font=('Arial', 10), 
                bg=self.bg_color, fg=self.text_color).pack()
        date_frame = tk.Frame(self.frame, bg=self.bg_color)
        date_frame.pack()

        self.day_entry = tk.Entry(date_frame, width=4)
        self.month_entry = tk.Entry(date_frame, width=4)
        self.year_entry = tk.Entry(date_frame, width=6)

        self.day_entry.pack(side=tk.LEFT)
        tk.Label(date_frame, text="/", bg=self.bg_color, fg=self.text_color).pack(side=tk.LEFT)
        self.month_entry.pack(side=tk.LEFT)
        tk.Label(date_frame, text="/", bg=self.bg_color, fg=self.text_color).pack(side=tk.LEFT)
        self.year_entry.pack(side=tk.LEFT)

        # Input cerita
        tk.Label(self.frame, text="Ada cerita apa hari ini?", font=('Arial', 10), 
                bg=self.bg_color, fg=self.text_color).pack()
        self.story_entry = tk.Entry(self.frame, width=40)
        self.story_entry.pack()

        # Input mood
        tk.Label(self.frame, text="Bagaimana perasaanmu?", font=('Arial', 10), 
                bg=self.bg_color, fg=self.text_color).pack()
        self.mood_var = tk.StringVar()
        self.mood_options = ["😌", "🙂", "😍", "😞", "😡"]
        self.mood_descriptions = {
            "😌": "Tenang dan damai",
            "🙂": "Baik-baik saja",
            "😍": "Sangat bahagia",
            "😞": "Sedih atau kecewa",
            "😡": "Marah atau frustasi"
        }
        mood_frame = tk.Frame(self.frame, bg=self.bg_color)
        mood_frame.pack()
        for mood in self.mood_options:
            tk.Radiobutton(mood_frame, text=mood, variable=self.mood_var, 
                          value=mood, bg=self.bg_color, fg=self.text_color).pack(side=tk.LEFT)

        # Tombol Simpan & Riwayat
        button_frame = tk.Frame(self.frame, pady=10, bg=self.bg_color)
        button_frame.pack()
        tk.Button(button_frame, text="Riwayat", command=self.show_history, 
                 bg=self.button_color, fg=self.text_color).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Simpan", command=self.save_mood, 
                 bg=self.button_color, fg=self.text_color).pack(side=tk.LEFT)

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
            datetime.strptime(date, "%Y-%m-%d")  # Validasi format tanggal
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
        top.configure(bg=self.bg_color)
        tk.Label(top, text="Seperti apa kamu ingin riwayatmu ditampilkan?", 
               bg=self.bg_color, fg=self.text_color).pack(pady=10)
        tk.Button(top, text="Per minggu", command=lambda: display("week"), 
                 bg=self.button_color, fg=self.text_color).pack(pady=5)
        tk.Button(top, text="Per bulan", command=lambda: display("month"), 
                 bg=self.button_color, fg=self.text_color).pack(pady=5)
        tk.Button(top, text="Batal", command=top.destroy, 
                 bg=self.button_color, fg=self.text_color).pack(pady=5)

    # Tampilkan data mood dan cerita
    def render_history(self, mode):
        top = tk.Toplevel(self.root)
        top.title("Riwayat")
        top.configure(bg=self.bg_color)

        text_area = tk.Text(top, wrap=tk.WORD, width=60, height=25, 
                           bg="#fff9e6", fg=self.text_color)
        text_area.pack(pady=10, padx=10)

        mood_list = load_data()
        mood_list.sort_by_date()  # Sorting data sebelum ditampilkan

        data = mood_list.to_list()
        
        mood_count = {mood: 0 for mood in self.mood_options}
        stories = []

        # Ambil data terakhir 7 hari atau 30 hari
        if mode == "week":
            filtered = data[-7:] if len(data) >= 7 else data
        else:
            filtered = data[-30:] if len(data) >= 30 else data

        for entry in filtered:
            mood_count[entry['mood']] += 1
            stories.append(entry['story'])

        # Hitung total mood untuk perhitungan sorting
        total_moods = sum(mood_count.values())
        
        summary = "=== REKAPAN MOOD ===\n\n"
        
        # Tampilkan deskripsi masing-masing emoji
        summary += "Deskripsi Mood:\n"
        for mood in self.mood_options:
            summary += f"{mood}: {self.mood_descriptions[mood]}\n"
        
        summary += "\n=== STATISTIK ===\n\n"
        
        if filtered:
            # Urutkan berdasarkan jumlah mood terbanyak
            sorted_moods = sorted(mood_count.items(), key=lambda x: x[1], reverse=True)
            
            # Tampilkan statistik mood
            for mood, count in sorted_moods:
                if total_moods > 0:
                    percentage = (count / total_moods) * 100
                    summary += f"{mood} : {count} kali ({percentage:.1f}%)\n"
                else:
                    summary += f"{mood} : 0 kali (0%)\n"
            
            # Tampilkan mood yang paling sering muncul
            most_common_mood = sorted_moods[0][0]
            summary += f"\nMood yang paling sering: {most_common_mood}\n"
            
            # Berikan motivasi berdasarkan mood yang paling sering
            motivation = self.get_motivation(most_common_mood)
            summary += f"\n=== MOTIVASI ===\n\n{motivation}\n"
            
            summary += "\n=== CERITA TERAKHIR ===\n\n"
            summary += f"{filtered[-1]['date']} - {filtered[-1]['mood']}:\n"
            summary += f"{filtered[-1]['story']}\n"
        else:
            summary += "Belum ada data mood yang tersimpan.\n"

        text_area.insert(tk.END, summary)
        text_area.config(state=tk.DISABLED)

        # Frame untuk tombol
        button_frame = tk.Frame(top, bg=self.bg_color)
        button_frame.pack(pady=10)

        # Tombol cari keyword
        def cari():
            keyword = simpledialog.askstring("Cari Cerita", "Masukkan keyword:")
            if keyword:
                result_list = mood_list.search_by_keyword(keyword)
                result = result_list.to_list()
                
                # Buat window baru untuk hasil pencarian
                result_window = tk.Toplevel(top)
                result_window.title("Hasil Pencarian")
                result_window.configure(bg=self.bg_color)
                
                text_result = tk.Text(result_window, wrap=tk.WORD, width=60, height=15, 
                                    bg="#fff9e6", fg=self.text_color)
                text_result.pack(pady=10, padx=10)
                
                if result:
                    hasil = f"Hasil pencarian '{keyword}':\n\n"
                    for r in result:
                        hasil += f"{r['date']} - {r['mood']}:\n{r['story']}\n\n"
                else:
                    hasil = f"Tidak ditemukan cerita dengan keyword '{keyword}'"
                
                text_result.insert(tk.END, hasil)
                text_result.config(state=tk.DISABLED)
                
                tk.Button(result_window, text="Tutup", command=result_window.destroy, 
                         bg=self.button_color, fg=self.text_color).pack(pady=5)

        tk.Button(button_frame, text="Cari Cerita", command=cari, 
                 bg=self.button_color, fg=self.text_color).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Tutup", command=top.destroy, 
                 bg=self.button_color, fg=self.text_color).pack(side=tk.LEFT, padx=5)

    def get_motivation(self, most_common_mood):
        motivations = {
            "😌": "Kamu tampaknya sering merasa tenang dan damai. Pertahankan energi positifmu ini!",
            "🙂": "Kamu sering merasa baik-baik saja. Jangan lupa untuk mencari kebahagiaan dalam hal-hal kecil sehari-hari.",
            "😍": "Wah, kamu sering merasa sangat bahagia! Bagikan kebahagiaanmu dengan orang-orang di sekitarmu.",
            "😞": "Kamu sering merasa sedih akhir-akhir ini. Ingatlah bahwa setiap hari adalah kesempatan baru. Kamu lebih kuat dari yang kamu kira!",
            "😡": "Kamu tampaknya sering merasa marah atau frustrasi. Cobalah untuk menemukan sumber masalahnya dan bicarakan dengan orang yang kamu percaya."
        }
        return motivations.get(most_common_mood, "Teruslah mengekspresikan perasaanmu. Setiap emosi adalah bagian dari pengalaman hidup yang berharga.")

# Jalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = MoodTrackerApp(root)
    root.mainloop()