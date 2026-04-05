import yt_dlp
import os

def download_mp3(url:str, output_path:str ="Z:\\TaiLieu\\Data",quality: str = "128"):
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting to MP3 ...')
        elif d['status'] == 'downloading':
            print(f"\r⬇ Downloading... {d.get('_percent_str', '?')} "
                  f"at {d.get('_speed_str', '?')}", end="")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        },
        {
            'key': 'EmbedThumbnail',
        },
        {
            'key': 'FFmpegMetadata',   # Embed title, artist, etc.
            'add_metadata': True,
        },
        ],
        'writethumbnail': True,    # Needed for EmbedThumbnail
        'progress_hooks': [my_hook],
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Unknown Title')
            print(f"\n✅ Downloaded and converted: {title}.mp3")
            return True
    except yt_dlp.utils.DownloadError as de:
        print(f"\n❌ Download error: {de}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def batch_download(urls:list, output_path:str ="Z:\\TaiLieu\\Data", quality: str = "128"):
    os.makedirs(output_path, exist_ok=True)
    print(f"📁 Saving to: {output_path}")
    successed, failed = 0, 0
    for i, url in enumerate(urls, 1):
        print(f"\n🔹 Processing {i}/{len(urls)}: {url}")
        if download_mp3(url, output_path, quality):
            successed += 1
        else:
            failed += 1

if __name__ == "__main__":
    # Batch download
    buitruonglinh = [
        "https://youtu.be/3CSNJ5_TCbY?si=5bV_lBivixpH0z_d",
        "https://youtu.be/-dsIiSaPZZA?si=IdSmEL5eu4KR4QbU",
        "https://youtu.be/FvWPSA2mt2s?si=Fne31Kb-VCtZ9Hj5",
        "https://youtu.be/KIIgt2VY-u0?si=EpYyhkYA1FyAQ21l",
        "https://youtu.be/rym-6cROUwk?si=3n8R-aRmoAMlfYyb",
    ]
    marzuz = [
        "https://youtu.be/foRDalDXOQU?si=GeAK4to4ROMy6Dor",
        "https://youtu.be/rXkF6uu-rFY?si=DTuwIC9heomNn_Ko",
        "https://youtu.be/ygAAdtRHp3w?si=ekupNW7jWGOTUJee",
        "https://youtu.be/ULxdO3OUypw?si=7IkR7Sazi14JuBeA",
        "https://youtu.be/uyR8V4hGrTk?si=dy838jh-D6rje-cv",
        "https://youtu.be/bWEw9hL3eJo?si=NWO3ssDo620NCtF6",
        "https://youtu.be/OfHCnuvrPLM?si=4UsWckFFmZ_4WrFf",
        "https://youtu.be/A-qbw1Mnjxw?si=N2FjUrB_p5C983Wj",
        "https://youtu.be/0fh8tDAtSEs?si=X7Y00EdpMz46-seM",
        "https://youtu.be/sKtGVyW4c08?si=8749EU2S1oT4Yl4Y"
    ]

    singers = {
        "buitruonglinh": buitruonglinh,
        "marzuz": marzuz,
        
    }

    base_path = "Z:\\TaiLieu\\Data"
    for name, urls in singers.items():
        batch_download(urls, output_path=os.path.join(base_path, name), quality="128")

    