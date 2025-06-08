import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import json
from datetime import datetime, timedelta

DATA_FILE = 'data.json'
LOGO_PATH = 'logo_unesa.png'

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class MoodLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

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

    def to_list(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

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

    def search_by_keyword(self, keyword):
        results = MoodLinkedList()
        curr = self.head
        while curr:
            if keyword.lower() in curr.data['story'].lower():
                results.append(curr.data)
            curr = curr.next
        return results

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

def save_data(mood_list):
    with open(DATA_FILE, 'w') as f:
        json.dump(mood_list.to_list(), f, indent=2)

def add_entry(date, story, mood):
    mood_list = load_data()
    mood_list.append({"date": date, "story": story, "mood": mood})
    save_data(mood_list)

class MoodTrackerApp:
    def __init__(self, root):
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

        try:
            logo = Image.open(LOGO_PATH)
            logo = logo.resize((70, 70))
            self.logo_img = ImageTk.PhotoImage(logo)
            tk.Label(self.root, image=self.logo_img, bg=self.bg_color).place(relx=1.0, x=-10, y=10, anchor='ne')
        except:
            pass

        tk.Label(self.frame, text="Mood Tracker", font=('Arial', 20, 'bold'), bg=self.bg_color, fg=self.text_color).pack()
        tk.Label(self.frame, text="Aplikasi ini membantu pengguna memantau kondisi emosional Anda dari waktu ke waktu\n"
                                  "melalui pencatatan dan analisis sederhana dengan pendekatan yang lebih praktis dan efisien.",
                 font=('Arial', 10), bg=self.bg_color, fg=self.text_color, justify="center").pack(pady=5)

        tk.Label(self.frame, text="Tanggal hari ini:", bg=self.bg_color, fg=self.text_color).pack()
        self.date_entry = DateEntry(self.frame, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
        self.date_entry.pack(pady=2)

        tk.Label(self.frame, text="Ada cerita apa hari ini?", bg=self.bg_color, fg=self.text_color).pack()
        self.story_entry = tk.Entry(self.frame, width=50)
        self.story_entry.pack()

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

        button_frame = tk.Frame(self.frame, bg=self.bg_color)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Simpan", command=self.save_mood, bg=self.button_color).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Riwayat", command=self.show_history_options, bg=self.button_color).pack(side=tk.LEFT, padx=10)

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

    def show_history_options(self):
        top = tk.Toplevel(self.root)
        top.title("Pilih Riwayat")
        top.geometry("400x200")
        top.configure(bg=self.bg_color)

        tk.Label(top, text="Pilih Jenis Riwayat", font=('Arial', 14), bg=self.bg_color, fg=self.text_color).pack(pady=20)

        button_frame = tk.Frame(top, bg=self.bg_color)
        button_frame.pack()

        tk.Button(button_frame, text="Mingguan", command=lambda: [top.destroy(), self.show_history("weekly")], 
                 bg=self.button_color, width=15).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="Bulanan", command=lambda: [top.destroy(), self.show_history("monthly")], 
                 bg=self.button_color, width=15).pack(side=tk.LEFT, padx=10, pady=10)

    def show_history(self, period_type):
        top = tk.Toplevel(self.root)
        # Corrected window title
        top_title = "Riwayat Mingguan" if period_type == "weekly" else "Riwayat Bulanan"
        top.title(top_title)
        top.geometry("800x600")
        top.configure(bg=self.bg_color)

        try:
            logo = Image.open(LOGO_PATH)
            logo = logo.resize((40, 40))
            self.logo_img2 = ImageTk.PhotoImage(logo)
            tk.Label(top, image=self.logo_img2, bg=self.bg_color).place(relx=1.0, x=-50, y=10, anchor='ne')
        except:
            pass

        main_frame = tk.Frame(top, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        stats_frame = tk.Frame(main_frame, bg=self.bg_color)
        stats_frame.pack(fill=tk.X, pady=10)

        mood_list = load_data()
        mood_list.sort_by_date()
        data = mood_list.to_list()

        today = datetime.now().date()
        
        if period_type == "weekly":
            period_start = today - timedelta(days=7)
            period_title = "Mingguan"
        else:  # monthly
            period_start = today - timedelta(days=30)
            period_title = "Bulanan"

        period_data = [entry for entry in data 
                      if datetime.strptime(entry['date'], "%Y-%m-%d").date() >= period_start]

        mood_count = {m: 0 for m in self.mood_options}
        for entry in period_data:
            mood_count[entry['mood']] += 1

        total = sum(mood_count.values())
        sorted_mood = sorted(mood_count.items(), key=lambda x: x[1], reverse=True)
        most_common = sorted_mood[0][0] if sorted_mood else ""

        stats_text = tk.Text(stats_frame, wrap=tk.WORD, width=70, height=8, 
                            bg="#fff9e6", fg=self.text_color, font=('Arial', 10))
        stats_text.pack(fill=tk.X)

        stats_summary = f"=== Statistik Mood {period_title} ===\n\n"
        for mood, count in sorted_mood:
            percent = (count / total * 100) if total > 0 else 0
            stats_summary += f"{mood} ({self.mood_descriptions[mood]}): {count} kali ({percent:.1f}%)\n"

        stats_summary += f"\nRata-rata mood kamu: {most_common} ({self.mood_descriptions.get(most_common, '-')})\n"
        stats_summary += f"\nMotivasi untukmu:\n{self.get_motivation(most_common)}\n"

        stats_text.insert(tk.END, stats_summary)
        stats_text.config(state=tk.DISABLED)

        history_frame = tk.Frame(main_frame, bg=self.bg_color)
        history_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(history_frame, columns=('Date', 'Mood', 'Story'), show='headings', height=10)
        tree.heading('Date', text='Tanggal')
        tree.heading('Mood', text='Mood')
        tree.heading('Story', text='Cerita')
        tree.column('Date', width=100)
        tree.column('Mood', width=80)
        tree.column('Story', width=300)

        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)

        for entry in period_data:
            tree.insert('', tk.END, values=(entry['date'], entry['mood'], entry['story']))

        tk.Button(main_frame, text="Ekspor ke CSV", command=lambda: self.export_period_data(period_data, period_title), 
                 bg=self.button_color).pack(pady=10)

        tk.Button(main_frame, text="Cari Cerita", command=lambda: self.search_story(mood_list), 
                 bg=self.button_color).pack(pady=5)

    def export_period_data(self, period_data, period_title):
        try:
            filename = f"mood_{period_title.lower()}_{datetime.now().strftime('%Y%m%d')}.csv"
            with open(filename, 'w') as f:
                f.write("Tanggal,Mood,Cerita\n")
                for entry in period_data:
                    story = entry['story'].replace('"', '""')
                    if ',' in story or '"' in story:
                        story = f'"{story}"'
                    f.write(f"{entry['date']},{entry['mood']},{story}\n")
            messagebox.showinfo("Sukses", f"Data {period_title.lower()} berhasil diekspor ke {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengekspor data: {str(e)}")

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

    def get_motivation(self, mood):
        motivasi = {
             "😄": "Wah keren sekali, tetap bahagia ya! Senyummu itu menular, semoga harimu selalu cerah!",
             "😩": "Ingat, istirahat itu penting. Semoga kamu segera merasa lebih segar dan semangat lagi!",
             "😐": "Hari-hari biasa juga berarti kamu stabil, terus jalani dengan santai dan jangan lupa bahagia ya!",
             "😢": "Sedih itu hal biasa, jangan dipikirin terlalu berat. Istirahat dulu kalau perlu, nanti juga akan lewat kok.",
             "😡": "Tenang dulu, yuk coba tarik napas dalam-dalam. Jangan biarkan amarah menguasaimu, kamu kuat kok!"
        }
        return motivasi.get(mood, "Tetaplah menulis dan sadari perasaanmu setiap hari.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MoodTrackerApp(root)
    root.mainloop()