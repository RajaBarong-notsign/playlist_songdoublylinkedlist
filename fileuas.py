import csv
import random
from datetime import datetime

# ==================== CLASS SONG ====================
class Song:
    """Class untuk merepresentasikan data lagu"""
    def __init__(self, id, title, artist, album, genre, duration, year, rating=0):
        self.id = id
        self.title = title
        self.artist = artist
        self.album = album
        self.genre = genre
        self.duration = duration  # dalam detik
        self.year = year
        self.rating = rating
    
    def __str__(self):
        return f"{self.id} | {self.title} | {self.artist} | {self.album} | {self.genre} | {self.duration}s | {self.year} | ⭐{self.rating}"


# ==================== CLASS NODE ====================
class Node:
    """Class Node untuk Doubly Linked List"""
    def __init__(self, song):
        self.song = song
        self.next = None
        self.prev = None


# ==================== CLASS DOUBLY LINKED LIST ====================
class DoublyLinkedList:
    """Class Doubly Linked List untuk Playlist Musik"""
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.current_song = None
    
    # ========== INSERT FUNCTIONS ==========
    def insert_first(self, song):
        """
        Menambahkan lagu di awal playlist
        Input: Song object
        Output: Boolean (True jika berhasil)
        Kompleksitas: O(1)
        """
        new_node = Node(song)
        
        if not self.head:  # Jika playlist kosong
            self.head = self.tail = new_node
            self.current_song = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        
        self.size += 1
        return True
    
    def insert_last(self, song):
        """
        Menambahkan lagu di akhir playlist
        Input: Song object
        Output: Boolean (True jika berhasil)
        Kompleksitas: O(1)
        """
        new_node = Node(song)
        
        if not self.tail:  # Jika playlist kosong
            self.head = self.tail = new_node
            self.current_song = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        
        self.size += 1
        return True
    
    def insert_after(self, target_id, song):
        """
        Menambahkan lagu setelah lagu dengan ID tertentu
        Input: target_id (String), Song object
        Output: Boolean (True jika berhasil, False jika target tidak ditemukan)
        Kompleksitas: O(n)
        """
        current = self.head
        
        while current:
            if current.song.id == target_id:
                new_node = Node(song)
                new_node.next = current.next
                new_node.prev = current
                
                if current.next:
                    current.next.prev = new_node
                else:
                    self.tail = new_node
                
                current.next = new_node
                self.size += 1
                return True
            
            current = current.next
        
        return False
    
    # ========== DELETE FUNCTIONS ==========
    def delete_first(self):
        """
        Menghapus lagu pertama dari playlist
        Input: -
        Output: Song object yang dihapus atau None
        Kompleksitas: O(1)
        """
        if not self.head:
            return None
        
        deleted = self.head.song
        
        if self.head == self.tail:  # Hanya 1 node
            self.head = self.tail = None
            self.current_song = None
        else:
            if self.current_song == self.head:
                self.current_song = self.head.next
            
            self.head = self.head.next
            self.head.prev = None
        
        self.size -= 1
        return deleted
    
    def delete_last(self):
        """
        Menghapus lagu terakhir dari playlist
        Input: -
        Output: Song object yang dihapus atau None
        Kompleksitas: O(1)
        """
        if not self.tail:
            return None
        
        deleted = self.tail.song
        
        if self.head == self.tail:  # Hanya 1 node
            self.head = self.tail = None
            self.current_song = None
        else:
            if self.current_song == self.tail:
                self.current_song = self.tail.prev
            
            self.tail = self.tail.prev
            self.tail.next = None
        
        self.size -= 1
        return deleted
    
    def delete_node(self, id):
        """
        Menghapus lagu berdasarkan ID
        Input: id (String)
        Output: Song object yang dihapus atau None
        Kompleksitas: O(n)
        """
        current = self.head
        
        while current:
            if current.song.id == id:
                # Jika node yang dihapus adalah head
                if current == self.head:
                    return self.delete_first()
                
                # Jika node yang dihapus adalah tail
                elif current == self.tail:
                    return self.delete_last()
                
                # Node di tengah
                else:
                    if self.current_song == current:
                        self.current_song = current.next or current.prev
                    
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    self.size -= 1
                    return current.song
            
            current = current.next
        
        return None
    
    # ========== DISPLAY FUNCTIONS ==========
    def display_forward(self):
        """
        Menampilkan playlist dari awal ke akhir
        Input: -
        Output: List of Song objects
        Kompleksitas: O(n)
        """
        songs = []
        current = self.head
        
        while current:
            songs.append(current.song)
            current = current.next
        
        return songs
    
    def display_backward(self):
        """
        Menampilkan playlist dari akhir ke awal
        Input: -
        Output: List of Song objects
        Kompleksitas: O(n)
        """
        songs = []
        current = self.tail
        
        while current:
            songs.append(current.song)
            current = current.prev
        
        return songs
    
    # ========== SEARCH & UPDATE FUNCTIONS ==========
    def search(self, query):
        """
        Mencari lagu berdasarkan judul, artis, atau genre
        Input: query (String)
        Output: List of Song objects yang cocok
        Kompleksitas: O(n)
        """
        results = []
        current = self.head
        query_lower = query.lower()
        
        while current:
            song = current.song
            if (query_lower in song.title.lower() or 
                query_lower in song.artist.lower() or 
                query_lower in song.genre.lower()):
                results.append(song)
            
            current = current.next
        
        return results
    
    def update(self, id, **kwargs):
        """
        Mengupdate informasi lagu berdasarkan ID
        Input: id (String), **kwargs (atribut yang ingin diupdate)
        Output: Boolean (True jika berhasil)
        Kompleksitas: O(n)
        """
        current = self.head
        
        while current:
            if current.song.id == id:
                for key, value in kwargs.items():
                    if hasattr(current.song, key):
                        setattr(current.song, key, value)
                return True
            
            current = current.next
        
        return False
    
    # ========== ADDITIONAL FEATURES ==========
    def shuffle(self):
        """
        Mengacak urutan playlist
        Input: -
        Output: Boolean (True jika berhasil)
        Kompleksitas: O(n)
        """
        songs = self.display_forward()
        random.shuffle(songs)
        
        # Rebuild playlist
        self.head = self.tail = None
        self.current_song = None
        self.size = 0
        
        for song in songs:
            self.insert_last(song)
        
        return True
    
    def play_next(self):
        """
        Memutar lagu berikutnya
        Input: -
        Output: Song object atau None
        Kompleksitas: O(1)
        """
        if self.current_song and self.current_song.next:
            self.current_song = self.current_song.next
            return self.current_song.song
        return None
    
    def play_previous(self):
        """
        Memutar lagu sebelumnya
        Input: -
        Output: Song object atau None
        Kompleksitas: O(1)
        """
        if self.current_song and self.current_song.prev:
            self.current_song = self.current_song.prev
            return self.current_song.song
        return None
    
    def get_current_song(self):
        """
        Mendapatkan lagu yang sedang diputar
        Input: -
        Output: Song object atau None
        Kompleksitas: O(1)
        """
        return self.current_song.song if self.current_song else None
    
    def get_total_duration(self):
        """
        Menghitung total durasi playlist
        Input: -
        Output: Integer (total durasi dalam detik)
        Kompleksitas: O(n)
        """
        total = 0
        current = self.head
        
        while current:
            total += current.song.duration
            current = current.next
        
        return total
    
    def filter_by_genre(self, genre):
        """
        Filter lagu berdasarkan genre
        Input: genre (String)
        Output: List of Song objects
        Kompleksitas: O(n)
        """
        results = []
        current = self.head
        
        while current:
            if current.song.genre.lower() == genre.lower():
                results.append(current.song)
            current = current.next
        
        return results
    
    def filter_by_year(self, year):
        """
        Filter lagu berdasarkan tahun
        Input: year (Integer)
        Output: List of Song objects
        Kompleksitas: O(n)
        """
        results = []
        current = self.head
        
        while current:
            if current.song.year == year:
                results.append(current.song)
            current = current.next
        
        return results
    
    def sort_by_title(self):
        """
        Sort playlist berdasarkan judul (A-Z)
        Input: -
        Output: Boolean
        Kompleksitas: O(n log n)
        """
        songs = self.display_forward()
        songs.sort(key=lambda x: x.title.lower())
        
        # Rebuild playlist
        self.head = self.tail = None
        self.current_song = None
        self.size = 0
        
        for song in songs:
            self.insert_last(song)
        
        return True
    
    def sort_by_artist(self):
        """
        Sort playlist berdasarkan artis (A-Z)
        Input: -
        Output: Boolean
        Kompleksitas: O(n log n)
        """
        songs = self.display_forward()
        songs.sort(key=lambda x: x.artist.lower())
        
        # Rebuild playlist
        self.head = self.tail = None
        self.current_song = None
        self.size = 0
        
        for song in songs:
            self.insert_last(song)
        
        return True


# ==================== UTILITY FUNCTIONS ====================
def parse_duration(duration_str):
    """Convert duration string (MM:SS) to seconds"""
    try:
        parts = duration_str.split(':')
        if len(parts) == 2:
            minutes = int(parts[0])
            seconds = int(parts[1])
            return minutes * 60 + seconds
        return 180  # default 3 menit
    except:
        return 180


def convert_txt_to_csv(input_file="DATASETUAS.txt", output_file="DATASETUAS.csv"):
    """
    Mengkonversi file TXT ke CSV
    Input: nama file txt, nama file csv output
    Output: Boolean
    """
    try:
        # File sudah dalam format CSV, tinggal copy dengan nama baru
        with open(input_file, 'r', encoding='utf-8') as infile:
            with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
                outfile.write(infile.read())
        
        print(f"✅ File berhasil dikonversi ke {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error konversi: {e}")
        return False


def load_from_csv(filename):
    """Memuat playlist dari file CSV/TXT"""
    playlist = DoublyLinkedList()
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                try:
                    # Parse duration dari format MM:SS ke detik
                    duration = parse_duration(row['Duration'])
                    
                    song = Song(
                        id=str(row['ID']),
                        title=row['Title'],
                        artist=row['Artist'],
                        album=row['Album'],
                        genre=row['Genre'],
                        duration=duration,
                        year=int(row['Year']),
                        rating=float(row['Rating'])
                    )
                    playlist.insert_last(song)
                    count += 1
                except Exception as e:
                    print(f"⚠️  Error parsing row {count+1}: {e}")
                    continue
        
        print(f"✅ Berhasil memuat {count} lagu dari {filename}")
        return playlist
    except FileNotFoundError:
        print(f"❌ File {filename} tidak ditemukan")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def save_to_csv(playlist, filename="playlist_export.csv"):
    """Menyimpan playlist ke file CSV"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Title', 'Artist', 'Album', 'Genre', 'Duration', 'Year', 'Rating'])
            
            songs = playlist.display_forward()
            for song in songs:
                duration_str = format_duration(song.duration)
                writer.writerow([song.id, song.title, song.artist, song.album, 
                               song.genre, duration_str, song.year, song.rating])
        
        print(f"✅ Playlist berhasil disimpan ke {filename}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def format_duration(seconds):
    """Format durasi dari detik ke MM:SS"""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"


def print_songs(songs, title="Playlist", limit=20):
    """Menampilkan daftar lagu dalam format tabel"""
    if not songs:
        print("❌ Tidak ada lagu ditemukan")
        return
    
    print(f"\n{'='*130}")
    print(f"{title.center(130)}")
    print(f"{'='*130}")
    print(f"{'No':<5} {'ID':<8} {'Title':<30} {'Artist':<20} {'Genre':<15} {'Dur':<7} {'Year':<6} {'Rating':<8}")
    print(f"{'-'*130}")
    
    display_songs = songs[:limit] if len(songs) > limit else songs
    
    for i, song in enumerate(display_songs, 1):
        print(f"{i:<5} {str(song.id):<8} {song.title[:28]:<30} {song.artist[:18]:<20} "
              f"{song.genre[:13]:<15} {format_duration(song.duration):<7} {song.year:<6} {'⭐'*int(song.rating):<8}")
    
    if len(songs) > limit:
        print(f"\n... dan {len(songs) - limit} lagu lainnya")
    
    print(f"{'='*130}")
    print(f"Total: {len(songs)} lagu\n")


# ==================== MUSIC PLAYLIST SYSTEM ====================
class MusicPlaylistSystem:
    """Sistem Manajemen Playlist Musik"""
    
    def __init__(self):
        self.playlist = DoublyLinkedList()
        self.is_playing = False
    
    def show_menu(self):
        """Menampilkan menu utama"""
        print("\n" + "="*60)
        print("🎵  SISTEM MANAJEMEN PLAYLIST MUSIK  🎵".center(60))
        print("="*60)
        print("1.  Tambah Lagu di Awal (Insert First)")
        print("2.  Tambah Lagu di Akhir (Insert Last)")
        print("3.  Tambah Lagu Setelah Lagu Tertentu (Insert After)")
        print("4.  Hapus Lagu Pertama (Delete First)")
        print("5.  Hapus Lagu Terakhir (Delete Last)")
        print("6.  Hapus Lagu Tertentu (Delete Node)")
        print("7.  Tampilkan Playlist Maju (Display Forward)")
        print("8.  Tampilkan Playlist Mundur (Display Backward)")
        print("9.  Cari Lagu (Search)")
        print("10. Update Lagu (Update)")
        print("11. Shuffle Playlist")
        print("12. Play Next")
        print("13. Play Previous")
        print("14. Show Now Playing")
        print("15. Filter by Genre")
        print("16. Filter by Year")
        print("17. Sort by Title")
        print("18. Sort by Artist")
        print("19. Show Statistics")
        print("20. Export to CSV")
        print("21. Load Data dari File")
        print("22. Convert TXT to CSV")
        print("0.  Keluar")
        print("="*60)
    
    def add_song_manual(self):
        """Input manual untuk menambah lagu"""
        print("\n--- Tambah Lagu Baru ---")
        id = f"song_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        title = input("Judul: ")
        artist = input("Artis: ")
        album = input("Album: ")
        genre = input("Genre: ")
        duration = int(input("Durasi (detik): "))
        year = int(input("Tahun: "))
        rating = float(input("Rating (1-5): "))
        
        return Song(id, title, artist, album, genre, duration, year, rating)
    
    def run(self):
        """Menjalankan sistem"""
        # Auto-load data saat pertama kali jalan
        print("\n🔄 Mencoba memuat data dari file DATASETUAS.txt...")
        loaded_playlist = load_from_csv("DATASETUAS.txt")
        if loaded_playlist:
            self.playlist = loaded_playlist
            print(f"📊 Total lagu dalam playlist: {self.playlist.size}")
        else:
            print("⚠️  File tidak ditemukan. Playlist kosong.")
            print("💡 Tip: Letakkan file DATASETUAS.txt di folder yang sama dengan script ini")
        
        while True:
            self.show_menu()
            choice = input("Pilih menu: ")
            
            if choice == '1':
                song = self.add_song_manual()
                self.playlist.insert_first(song)
                print("✅ Lagu berhasil ditambahkan di awal")
            
            elif choice == '2':
                song = self.add_song_manual()
                self.playlist.insert_last(song)
                print("✅ Lagu berhasil ditambahkan di akhir")
            
            elif choice == '3':
                target_id = input("ID lagu target: ")
                song = self.add_song_manual()
                if self.playlist.insert_after(target_id, song):
                    print("✅ Lagu berhasil ditambahkan")
                else:
                    print("❌ ID lagu tidak ditemukan")
            
            elif choice == '4':
                deleted = self.playlist.delete_first()
                if deleted:
                    print(f"✅ Lagu '{deleted.title}' berhasil dihapus")
                else:
                    print("❌ Playlist kosong")
            
            elif choice == '5':
                deleted = self.playlist.delete_last()
                if deleted:
                    print(f"✅ Lagu '{deleted.title}' berhasil dihapus")
                else:
                    print("❌ Playlist kosong")
            
            elif choice == '6':
                id = input("ID lagu yang akan dihapus: ")
                deleted = self.playlist.delete_node(id)
                if deleted:
                    print(f"✅ Lagu '{deleted.title}' berhasil dihapus")
                else:
                    print("❌ Lagu tidak ditemukan")
            
            elif choice == '7':
                songs = self.playlist.display_forward()
                limit = int(input("Tampilkan berapa lagu? (0=semua): ") or "20")
                if limit == 0:
                    limit = len(songs)
                print_songs(songs, "Playlist (Forward)", limit)
            
            elif choice == '8':
                songs = self.playlist.display_backward()
                limit = int(input("Tampilkan berapa lagu? (0=semua): ") or "20")
                if limit == 0:
                    limit = len(songs)
                print_songs(songs, "Playlist (Backward)", limit)
            
            elif choice == '9':
                query = input("Masukkan kata kunci (judul/artis/genre): ")
                results = self.playlist.search(query)
                print_songs(results, f"Hasil Pencarian: '{query}'", limit=len(results))  # Tampilkan semua  
            
            elif choice == '10':
                id = input("ID lagu yang akan diupdate: ")
                print("Masukkan data baru (kosongkan jika tidak ingin mengubah)")
                title = input("Judul baru: ")
                artist = input("Artis baru: ")
                genre = input("Genre baru: ")
                
                updates = {}
                if title: updates['title'] = title
                if artist: updates['artist'] = artist
                if genre: updates['genre'] = genre
                
                if self.playlist.update(id, **updates):
                    print("✅ Lagu berhasil diupdate")
                else:
                    print("❌ Lagu tidak ditemukan")
            
            elif choice == '11':
                self.playlist.shuffle()
                print("✅ Playlist berhasil di-shuffle")
            
            elif choice == '12':
                next_song = self.playlist.play_next()
                if next_song:
                    print(f"▶️  Now Playing: {next_song.title} - {next_song.artist}")
                else:
                    print("❌ Tidak ada lagu berikutnya")
            
            elif choice == '13':
                prev_song = self.playlist.play_previous()
                if prev_song:
                    print(f"▶️  Now Playing: {prev_song.title} - {prev_song.artist}")
                else:
                    print("❌ Tidak ada lagu sebelumnya")
            
            elif choice == '14':
                current = self.playlist.get_current_song()
                if current:
                    print(f"\n{'='*80}")
                    print(f"▶️  NOW PLAYING".center(80))
                    print(f"{'='*80}")
                    print(f"Title   : {current.title}")
                    print(f"Artist  : {current.artist}")
                    print(f"Album   : {current.album}")
                    print(f"Genre   : {current.genre}")
                    print(f"Duration: {format_duration(current.duration)}")
                    print(f"Year    : {current.year}")
                    print(f"Rating  : {'⭐' * int(current.rating)}")
                    print(f"{'='*80}\n")
                else:
                    print("❌ Tidak ada lagu yang sedang diputar")
            
            elif choice == '15':
                genre = input("Genre: ")
                results = self.playlist.filter_by_genre(genre)
                print_songs(results, f"Lagu Genre: {genre}", limit=len(results))  # Tampilkan semua
            
            elif choice == '16':
                year = int(input("Tahun: "))
                results = self.playlist.filter_by_year(year)
                print_songs(results, f"Lagu Tahun: {year}", limit=len(results))  # Tampilkan semua
            
            elif choice == '17':
                self.playlist.sort_by_title()
                print("✅ Playlist berhasil diurutkan berdasarkan judul")
            
            elif choice == '18':
                self.playlist.sort_by_artist()
                print("✅ Playlist berhasil diurutkan berdasarkan artis")
            
            elif choice == '19':
                total_songs = self.playlist.size
                total_duration = self.playlist.get_total_duration()
                current = self.playlist.get_current_song()
                
                print(f"\n{'='*60}")
                print(f"📊  STATISTIK PLAYLIST".center(60))
                print(f"{'='*60}")
                print(f"Total Lagu       : {total_songs}")
                print(f"Total Durasi     : {format_duration(total_duration)} ({total_duration} detik)")
                print(f"Rata-rata Durasi : {format_duration(total_duration // total_songs if total_songs > 0 else 0)}")
                print(f"Now Playing      : {current.title if current else 'Tidak ada'}")
                print(f"{'='*60}\n")
            
            elif choice == '20':
                filename = input("Nama file (default: playlist_export.csv): ") or "playlist_export.csv"
                save_to_csv(self.playlist, filename)
            
            elif choice == '21':
                filename = input("Nama file (default: DATASETUAS.txt): ") or "DATASETUAS.txt"
                loaded_playlist = load_from_csv(filename)
                if loaded_playlist:
                    self.playlist = loaded_playlist
            
            elif choice == '22':
                print("\n--- Konversi TXT ke CSV ---")
                input_file = input("File TXT input (default: DATASETUAS.txt): ") or "DATASETUAS.txt"
                output_file = input("File CSV output (default: DATASETUAS.csv): ") or "DATASETUAS.csv"
                convert_txt_to_csv(input_file, output_file)
            
            elif choice == '0':
                print("\n👋 Terima kasih telah menggunakan sistem ini!")
                break
            
            else:
                print("❌ Pilihan tidak valid!")
            
            input("\nTekan Enter untuk melanjutkan...")


# ==================== MAIN PROGRAM ====================
if __name__ == "__main__":
    system = MusicPlaylistSystem()
    system.run()


