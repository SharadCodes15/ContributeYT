#!/usr/bin/env python3
"""
YouTube Video/Audio Downloader with Quality Options
Supports single videos and entire playlists
Uses yt-dlp to download videos or extract audio as MP3
"""

import yt_dlp
import sys
import re
import os
import random
import time
import shutil


# ---------------
# Colors 
# ---------------

RESET = "\033[0m"
BOLD = "\033[1m"

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
WHITE = "\033[97m"
GRAY = "\033[90m"

# ---------------
# Terminal Helpers
# ---------------

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
def pause():
    input(f"\n{GRAY} Press Enter to Continue..... {RESET}")

def print_line(char='-',width=62):
    print(f"{CYAN}{char*width}{RESET}")

def print_box(title,width=62):
    print(f"{CYAN}╔{'═' * width}╗{RESET}")
    print(
        f"{CYAN}║{RESET}"
        f"{BOLD}{WHITE}{title.center(width)}{RESET}"
        f"{CYAN}║{RESET}"
    )
    print(f"{CYAN}╚{'═' * width}╝{RESET}")

# ---------------
# Header
# ---------------

def show_header():
    width = 62

    lines = [
    "██╗   ██╗████████╗██████╗ ",
    "╚██╗ ██╔╝╚══██╔══╝██╔══██╗",
    " ╚████╔╝    ██║   ██║  ██║",
    "  ╚██╔╝     ██║   ██║  ██║",
    "   ██║      ██║   ██████╔╝",
    "   ╚═╝      ╚═╝   ╚═════╝ ",
]

    print(f"{CYAN}╔{'═' * width}╗{RESET}")

    print(f"{CYAN}║{' ' * width}║{RESET}")

    for line in lines:
        print(
            f"{CYAN}║{RESET}"
            f"{BOLD}{WHITE}{line.center(width)}{RESET}"
            f"{CYAN}║{RESET}"
        )

    print(f"{CYAN}║{' ' * width}║{RESET}")

    print(
        f"{CYAN}║{RESET}"
        f"{BOLD}{WHITE}{'YouTube Video/Audio Downloader'.center(width)}{RESET}"
        f"{CYAN}║{RESET}"
    )

    print(
        f"{CYAN}║{RESET}"
        f"{WHITE}{'Supports Videos & Playlists'.center(width)}{RESET}"
        f"{CYAN}║{RESET}"
    )

    print(f"{CYAN}║{' ' * width}║{RESET}")

    print(f"{CYAN}╚{'═' * width}╝{RESET}")

# ---------------
# Menu
# ---------------

def show_menu():
    menu = [
        "[1]  Download YouTube Video / Playlist",
        "[2]  Download YouTube Audio (MP3)",
        "[3]  About",
        "[4]  Exit"
    ]

    width = 60

    print(f"\n{CYAN}{BOLD}")
    print("╔" + "═" * width + "╗")
    print("║" + "MAIN MENU".center(width) + "║")
    print("╠" + "═" * width + "╣")

    for item in menu:
        print("║   " + item.ljust(width - 3) + "║")

    print("╚" + "═" * width + "╝")
    print(RESET)

def about():
    """Display information about YTD."""

    width = 64

    print(f"\n{CYAN}╔{'═' * width}╗{RESET}")
    print(
        f"{CYAN}║{RESET}"
        f"{BOLD}{WHITE}{'ABOUT YTD'.center(width)}{RESET}"
        f"{CYAN}║{RESET}"
    )
    print(f"{CYAN}╠{'═' * width}╣{RESET}")

    about_lines = [
        "YTD - YouTube Video/Audio Downloader",
        "",
        "A simple terminal-based YouTube downloader",
        "powered by yt-dlp and FFmpeg.",
        "",
        "Features:",
        "• Download YouTube videos",
        "• Download videos as MP3 audio",
        "• Download entire playlists",
        "• Select specific playlist videos",
        "• Multiple video quality options",
        "• Multiple MP3 quality options",
        "",
        "Technologies:",
        "• Python",
        "• yt-dlp",
        "• FFmpeg",
    ]

    for line in about_lines:
        if len(line) > width - 1:
            line = line[:width - 5] + "..."

        print(
            f"{CYAN}║ {WHITE}{line.ljust(width - 1)}"
            f"{CYAN}║{RESET}"
        )

    print(f"{CYAN}╠{'═' * width}╣{RESET}")

    print(
        f"{CYAN}║"
        f"{GREEN}{'Thank you for using YTD!'.center(width)}"
        f"{CYAN}║{RESET}"
    )

    print(f"{CYAN}╚{'═' * width}╝{RESET}")

    pause()

def show_downloaded(location):
    """Show download completed message."""

    width = 64

    print(f"\n{GREEN}╔{'═' * width}╗{RESET}")
    print(
        f"{GREEN}║{BOLD}{WHITE}"
        f"{'DOWNLOAD COMPLETED'.center(width)}"
        f"{RESET}{GREEN}║{RESET}"
    )
    print(f"{GREEN}╠{'═' * width}╣{RESET}")

    message = "✓ Downloaded successfully!"

    print(
        f"{GREEN}║ {WHITE}{message}"
        f"{' ' * (width - len(message) - 3)}"
        f"{GREEN}║{RESET}"
    )

    if location:
        location = os.path.abspath(str(location))

        label = "Saved to:"
        max_location_length = width - len(label) - 6

        if len(location) > max_location_length:
            location = "..." + location[-(max_location_length - 3):]

        spaces = width - len(label) - len(location) - 5

        print(
            f"{GREEN}║ {YELLOW}{label}{RESET} "
            f"{WHITE}{location}"
            f"{' ' * max(1, spaces)}"
            f"{GREEN}║{RESET}"
        )
    else:
        fallback = "Current download folder"
        label = "Saved to:"
        spaces = max(1, width - len(label) - len(fallback) - 5)

        print(
            f"{GREEN}║ {YELLOW}{label}:{RESET} "
            f"{WHITE}{fallback}"
            f"{' ' * spaces}"
            f"{GREEN}║{RESET}"
        )


    print(f"{GREEN}╚{'═' * width}╝{RESET}")

    pause()

def thankyou():
    title = "Thank you for using Youtube Video Downloader!"
    goodbye = "Goodbye 👋"

    width = max(len(title), len(goodbye)) + 10

    print(f"""
{CYAN}╔{'═' * width}╗
║{' ' * width}║
║{BOLD}{WHITE}{title.center(width)}{RESET}{CYAN}║
║{' ' * width}║
║{goodbye.center(width)}║
║{' ' * width}║
╚{'═' * width}╝{RESET}
""")


# Path to cookies file - place cookies.txt in the same folder as this script
COOKIES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cookies.txt')
LAST_DOWNLOADED_FILE = None

# VPS-friendly options to help bypass YouTube restrictions
VPS_OPTIONS = {
    # Bypass geo-restrictions
    'geo_bypass': True,
    'geo_bypass_country': 'US',
    
    # Retry settings
    'retries': 10,
    'fragment_retries':  10,
    'file_access_retries': 5,
    
    # Sleep between requests to avoid rate limiting
    'sleep_interval': 1,
    'max_sleep_interval': 5,
    'sleep_interval_requests': 1,
    
    # HTTP settings
    'socket_timeout': 30,
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Sec-Fetch-Mode': 'navigate',
    },
}


def check_ffmpeg():
    """Check if ffmpeg is available for audio conversion"""
    return shutil.which('ffmpeg') is not None


def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        r'youtube\.com/v/([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def extract_playlist_id(url):
    """Extract playlist ID from YouTube URL"""
    # Match playlist ID (starts with PL, RD, UU, etc.)
    match = re.search(r'[?&]list=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    return None


def is_radio_playlist(playlist_id):
    """
    Check if playlist is a Radio/Mix (auto-generated, non-downloadable as playlist).
    Radio playlists start with 'RD' and are dynamically generated for each user.
    """
    if playlist_id:
        return playlist_id.startswith('RD')
    return False


def is_playlist_url(url):
    """Check if URL contains a playlist"""
    return 'list=' in url


def get_clean_video_url(video_id):
    """Get a clean video URL from video ID"""
    return f"https://www.youtube.com/watch?v={video_id}"


def get_playlist_url(playlist_id):
    """Get a playlist URL from playlist ID"""
    return f"https://www.youtube.com/playlist?list={playlist_id}"


def validate_url(url):
    """Validate YouTube URL"""
    url = url.strip()
    
    youtube_patterns = [
        r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+',
        r'^[a-zA-Z0-9_-]{11}$'
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, url):
            return True
    
    return False


def get_video_info(url, playlist_mode=False):
    """Get video/playlist information without downloading"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist' if playlist_mode else False,
        'skip_download': True,
        'ignoreerrors': True if playlist_mode else False,
        'noplaylist': not playlist_mode,
        **VPS_OPTIONS,
    }
    
    # Add cookies if file exists
    if os.path.exists(COOKIES_FILE):
        ydl_opts['cookiefile'] = COOKIES_FILE
        print(f"Using cookies from: {COOKIES_FILE}")
    else:
        print(f"Warning: cookies.txt not found at {COOKIES_FILE}")
    
    # Add random delay to avoid detection
    time.sleep(random.uniform(0.5, 2))
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Extracting information...")
            info = ydl.extract_info(url, download=False)
            
            if not info:
                print("Error: Could not extract information")
                return None
            
            return info
            
    except Exception as e:
        print(f"\n[ERROR] Error fetching information:")
        print(f"   {str(e)}")
        return None


def display_video_info(info):
    """Display video title and available formats"""

    title = info.get("title") or "Unknown"
    channel = info.get("channel") or info.get("uploader") or "Unknown"
    duration = info.get("duration") or 0

    # Format duration safely
    try:
        duration = int(duration)
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours:
            duration_str = f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            duration_str = f"{minutes}:{seconds:02d}"
    except (TypeError, ValueError):
        duration_str = "Unknown"

    # Display information
    print(f"\n{GREEN}╔{'═' * 64}╗{RESET}")
    print(f"{GREEN}║{'VIDEO INFORMATION'.center(64)}║{RESET}")
    print(f"{GREEN}╠{'═' * 64}╣{RESET}")

    # Title
    title_display = str(title)
    if len(title_display) > 53:
        title_display = title_display[:50] + "..."

    print(
        f"{GREEN}║ {YELLOW}Title:{RESET} "
        f"{title_display.ljust(55)}{GREEN}║{RESET}"
    )

    # Duration
    print(
        f"{GREEN}║ {YELLOW}Duration:{RESET} "
        f"{duration_str.ljust(52)}{GREEN}║{RESET}"
    )

    # Channel
    channel_display = str(channel)
    if len(channel_display) > 51:
        channel_display = channel_display[:48] + "..."

    print(
        f"{GREEN}║ {YELLOW}Channel:{RESET} "
        f"{channel_display.ljust(53)}{GREEN}║{RESET}"
    )

    print(f"{GREEN}╚{'═' * 64}╝{RESET}")



def display_playlist_info(info):
    """Display playlist information"""

    title = info.get("title", "Unknown")
    channel = info.get("channel") or info.get("uploader") or "Unknown"
    entries = info.get("entries") or []

    # Count only valid entries
    valid_entries = [entry for entry in entries if entry]
    video_count = len(valid_entries)

    # Build playlist information
    print(f"\n{GREEN}╔{'═' * 64}╗{RESET}")
    print(f"{GREEN}║{'PLAYLIST INFORMATION'.center(64)}║{RESET}")
    print(f"{GREEN}╠{'═' * 64}╣{RESET}")

    print(
        f"{GREEN}║ {YELLOW}Playlist:{RESET} "
        f"{title[:52].ljust(52)} {GREEN}║{RESET}"
    )

    print(
        f"{GREEN}║ {YELLOW}Videos:{RESET} "
        f"{str(video_count).ljust(56)} {GREEN}║{RESET}"
    )

    print(
        f"{GREEN}║ {YELLOW}Channel:{RESET} "
        f"{str(channel)[:51].ljust(51)} {GREEN}║{RESET}"
    )

    print(f"{GREEN}╠{'═' * 64}╣{RESET}")
    print(f"{GREEN}║{'VIDEOS IN PLAYLIST'.center(64)}║{RESET}")
    print(f"{GREEN}╠{'═' * 64}╣{RESET}")

    # Show first 10 videos
    for i, entry in enumerate(valid_entries[:10], 1):
        video_title = entry.get("title", "Unknown")

        if len(video_title) > 52:
            video_title = video_title[:52] + "..."

        line = f"{i:2}. {video_title}"

        print(
            f"{GREEN}║ {line.ljust(62)}║{RESET}"
        )

    if video_count > 10:
        more = f"... and {video_count - 10} more videos"
        print(f"{GREEN}║ {YELLOW}{more.ljust(62)}║{RESET}")

    print(f"{GREEN}╚{'═' * 64}╝{RESET}")

    return video_count



def download_video(url, quality='best', playlist_mode=False, playlist_items=None):
    """Download video with specified quality"""
    global LAST_DOWNLOADED_FILE
    LAST_DOWNLOADED_FILE = None
    quality_options = {
        'best': 'bestvideo+bestaudio/best',
        '2160p': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]',
        '1440p': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        '360p': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
    }
    
    format_string = quality_options.get(
        quality.lower(),
        quality_options['best']
    )
    
    output_template = (
        '%(playlist_title)s/%(title)s.%(ext)s'
        if playlist_mode
        else '%(title)s.%(ext)s'
    )
    
    ydl_opts = {
        'format': format_string,
        'outtmpl': output_template,
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
        'noplaylist': not playlist_mode,
        'ignoreerrors': True if playlist_mode else False,
        **VPS_OPTIONS,
    }
    
    if playlist_items:
        ydl_opts['playlist_items'] = playlist_items
    
    if os.path.exists(COOKIES_FILE):
        ydl_opts['cookiefile'] = COOKIES_FILE
    
    delay = random.uniform(1, 3)
    print(
        f"{YELLOW}Waiting {delay:.1f}s before starting download...{RESET}"
    )
    time.sleep(delay)
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        
            mode_text = "PLAYLIST" if playlist_mode else "VIDEO"
    
            print(
                f"\n{YELLOW}"
                f"Downloading {mode_text} "
                f"with quality: {quality}..."
                f"{RESET}"
            )
    
            result = ydl.download([url])
    
            if result == 0:
            
                # Use the filename captured by the progress hook
                location = LAST_DOWNLOADED_FILE
    
                if location:
                    location = os.path.abspath(location)
    
                show_downloaded(location)
    
                return True
    
            print(
                f"\n{RED}"
                f"✗ Download completed with errors."
                f"{RESET}"
            )
    
            return False
    
    except Exception as e:
    
        print(
            f"\n{RED}"
            f"[ERROR] Error downloading:"
            f"{RESET}"
        )
    
        print(f"   {str(e)}")
    
        return False

def download_audio(url, quality='320', playlist_mode=False, playlist_items=None):
    """Download audio and convert to MP3."""
    global LAST_DOWNLOADED_FILE
    LAST_DOWNLOADED_FILE = None
    audio_quality_map = {
        '320': '0',
        '256': '1',
        '192': '2',
        '128': '5',
        '96': '6',
        '64': '8',
    }

    quality_setting = audio_quality_map.get(quality, '0')

    output_template = (
        '%(playlist_title)s/%(title)s.%(ext)s'
        if playlist_mode
        else '%(title)s.%(ext)s'
    )

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'progress_hooks': [progress_hook],
        'noplaylist': not playlist_mode,
        'ignoreerrors': True if playlist_mode else False,
        **VPS_OPTIONS,

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality_setting,
        }],
    }

    if playlist_items:
        ydl_opts['playlist_items'] = playlist_items

    if os.path.exists(COOKIES_FILE):
        ydl_opts['cookiefile'] = COOKIES_FILE

    delay = random.uniform(1, 3)

    print(
        f"{YELLOW}"
        f"Waiting {delay:.1f}s before starting download..."
        f"{RESET}"
    )

    time.sleep(delay)

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            mode_text = (
                "PLAYLIST AUDIO"
                if playlist_mode
                else "AUDIO"
            )

            print(
                f"\n{GREEN}"
                f"Downloading {mode_text} "
                f"and converting to MP3 "
                f"({quality} kbps)..."
                f"{RESET}"
            )

            result = ydl.download([url])

            if result == 0:

                location = LAST_DOWNLOADED_FILE

                if location:
                    location = os.path.abspath(location)

                    # FFmpeg changes the final extension to .mp3
                    base, _ = os.path.splitext(location)
                    mp3_location = base + ".mp3"

                    if os.path.exists(mp3_location):
                        location = mp3_location

                show_downloaded(location)

                return True

            print(
                f"\n{RED}"
                f"✗ Download/conversion completed with errors."
                f"{RESET}"
            )

            return False

    except Exception as e:

        print(
            f"\n{RED}"
            f"[ERROR] Error downloading audio:"
            f"{RESET}"
        )

        print(f"   {str(e)}")

        return False

def progress_hook(d):
    global LAST_DOWNLOADED_FILE

    if d["status"] == "downloading":
        percent = d.get("_percent_str", "0%").strip()
        speed = d.get("_speed_str", "Unknown").strip()
        eta = d.get("_eta_str", "Unknown").strip()

        print(
            f"\r{CYAN}⬇{RESET} "
            f"{GREEN}{percent:>6}{RESET}  "
            f"{YELLOW}{speed:>12}{RESET}  "
            f"ETA: {eta:<8}",
            end="",
            flush=True
        )

    elif d["status"] == "finished":
        LAST_DOWNLOADED_FILE = d.get("filename")

        print(
            f"\r{GREEN}✓ Download finished! Processing...{RESET}"
            + " " * 20,
            flush=True
        )

    elif d["status"] == "error":
        print(
            f"\r{RED}✗ Download failed.{RESET}"
            + " " * 20,
            flush=True
        )


def select_video_quality():
    """Display video quality menu and get user choice"""
    menu_lines = [
        "Video Quality Options:",
        "",
        "1. Best available quality",
        "2. 2160p (4K)",
        "3. 1440p (2K)",
        "4. 1080p (Full HD)",
        "5. 720p (HD)",
        "6. 480p",
        "7. 360p",
    ]
    
    width = max(len(line) for line in menu_lines) + 4
    
    print(f"\n{CYAN}╔{'═' * width}╗{RESET}")
    
    for line in menu_lines:
        print(f"{CYAN}║ {line.ljust(width - 1)}║{RESET}")
    
    print(f"{CYAN}╚{'═' * width}╝{RESET}")

    
    video_choice = input(f"\n{YELLOW}Select video quality (1-7) [default: 1]: {RESET}").strip()
    
    video_quality_map = {
        '1': 'best',
        '2': '2160p',
        '3': '1440p',
        '4': '1080p',
        '5': '720p',
        '6': '480p',
        '7': '360p',
    }
    
    return video_quality_map.get(video_choice, 'best')


def select_audio_quality():
    """Display audio quality menu and get user choice"""
    menu_lines = [
        "Audio Quality Options (MP3):",
        "",
        "1. 320 kbps (Best quality)",
        "2. 256 kbps (High quality)",
        "3. 192 kbps (Good quality)",
        "4. 128 kbps (Medium quality)",
        "5. 96 kbps (Low quality)",
        "6. 64 kbps (Very low quality)",
    ]
    
    width = max(len(line) for line in menu_lines) + 4
    
    print(f"\n{CYAN}╔{'═' * width}╗{RESET}")
    
    for line in menu_lines:
        print(f"{CYAN}║ {line.ljust(width - 1)}║{RESET}")
    
    print(f"{CYAN}╚{'═' * width}╝{RESET}")

    
    audio_choice = input(f"\n{YELLOW}Select audio quality (1-6) [default: 1]: {RESET}").strip()
    
    audio_quality_map = {
        '1': '320',
        '2': '256',
        '3': '192',
        '4': '128',
        '5': '96',
        '6': '64',
    }
    
    return audio_quality_map.get(audio_choice, '320')

def urlInput():
    """Get and validate a YouTube URL."""

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input(
            f"\n{GREEN}Enter YouTube URL "
            f"(video or playlist): {RESET}"
        ).strip()

    if not url:
        print(f"{RED}✘ Error: No URL provided!{RESET}")
        return False

    if not validate_url(url):
        print(
            f"{RED}✘ Error: Invalid YouTube URL:{RESET}"
        )
        print(f"  {url}")
        return False

    process_url(url)


def process_url(url):
    original_url = url
    video_id = extract_video_id(url)
    playlist_id = extract_playlist_id(url)
    
    # Check if URL contains both video and playlist
    download_playlist = False
    playlist_items = None
    
    if playlist_id and video_id:
        # Check if it's a Radio/Mix playlist (cannot be downloaded as playlist)
        if is_radio_playlist(playlist_id):
            warning_lines = [
                "[WARNING] This is a Radio/Mix playlist (auto-generated).",
                "          Radio playlists cannot be downloaded as playlists.",
                "          Downloading single video only..."
            ]

            width = max(len(line) for line in warning_lines) + 4

            print(f"{YELLOW}╔{'═' * width}╗{RESET}")
            for line in warning_lines:
                print(f"{YELLOW}║ {line.ljust(width - 1)}║{RESET}")
            print(f"{YELLOW}╚{'═' * width}╝{RESET}")

            url = get_clean_video_url(video_id)
        else:
            # URL has both video and playlist - ask user what they want
            menu_lines = [
                "[INFO] This URL contains both a video and a playlist.",
                "",
                "What would you like to download?",
                "",
                "1. Single Video only",
                "2. Entire Playlist",
                "3. Select specific videos from playlist",
                ""
            ]

            width = max(len(line) for line in menu_lines) + 4

            print(f"\n{CYAN}╔{'═' * width}╗{RESET}")

            for line in menu_lines:
                print(f"{CYAN}║ {line.ljust(width - 1)}║{RESET}")

            print(f"{CYAN}╚{'═' * width}╝{RESET}")

            
            choice = input("\nSelect option (1-3) [default: 1]: ").strip()
            
            if choice == '2':
                download_playlist = True
                url = get_playlist_url(playlist_id)
                print(f"\n{YELLOW}[INFO] Will download entire playlist{RESET}")
            elif choice == '3':
                download_playlist = True
                url = get_playlist_url(playlist_id)
                playlist_items = input(f"\n{YELLOW}Enter video numbers to download (e.g., 1,3,5-10): {RESET}").strip()
                if not playlist_items:
                    playlist_items = None
                print(f"\n{YELLOW}[INFO] Will download selected videos from playlist{RESET}")
            else:
                url = get_clean_video_url(video_id)
                print(f"\n{YELLOW}[INFO] Will download single video{RESET}")
    
    elif playlist_id and not video_id:
        # Pure playlist URL
        download_playlist = True
        url = get_playlist_url(playlist_id)
        print(f"\n{YELLOW}[INFO] Playlist URL detected{RESET}")
        
        # Ask if they want the entire playlist
        menu_lines = [
            "Playlist Options:",
            "",
            "1. Download entire playlist",
            "2. Select specific videos",
        ]

        width = max(len(line) for line in menu_lines) + 4

        print(f"{CYAN}╔{'═' * width}╗{RESET}")

        for line in menu_lines:
            print(f"{CYAN}║ {line.ljust(width - 1)}║{RESET}")

        print(f"{CYAN}╚{'═' * width}╝{RESET}")
        
        choice = input(f"\n{YELLOW}Select option (1-2) [default: 1]: {RESET}").strip()
        
        if choice == '2':
            # First, get playlist info to show available videos
            info = get_video_info(url, playlist_mode=True)
            if info:
                video_count = display_playlist_info(info)
                playlist_items = input(f"\n{YELLOW}Enter video numbers to download (1-{video_count}, e.g., 1,3,5-10): {RESET}").strip()
                if not playlist_items:
                    playlist_items = None
    
    else:
        # Single video URL
        url = get_clean_video_url(video_id) if video_id else url
    
    print(f"\n{RED}Processing URL: {url}{RESET}")
    
    # Get info
    info = get_video_info(url, playlist_mode=download_playlist)
    if not info:
        return False
    
    # Display info
    if download_playlist:
        video_count = display_playlist_info(info)
    else:
        display_video_info(info)
    
    # Mode selection: Video or Audio
    menu_lines = [
        "Download Mode:",
        "",
        "1. VIDEO (MP4)",
        "2. AUDIO (MP3)",
    ]
    
    width = max(len(line) for line in menu_lines) + 4
    
    print(f"\n{CYAN}╔{'═' * width}╗{RESET}")
    
    for line in menu_lines:
        print(f"{CYAN}║ {line.ljust(width - 1)}║{RESET}")
    
    print(f"{CYAN}╚{'═' * width}╝{RESET}")

    
    mode_choice = input(f"\n{YELLOW}Select mode (1 for Video, 2 for Audio) [default: 1]: {RESET}").strip()

    print(f"{GREEN} DOWNLOADING.... {RESET}")
    if mode_choice == '2':
        # Audio mode
        audio_quality = select_audio_quality()
        success = download_audio(url, audio_quality, playlist_mode=download_playlist, playlist_items=playlist_items)
    else:
        # Video mode
        video_quality = select_video_quality()
        success = download_video(url, video_quality, playlist_mode=download_playlist, playlist_items=playlist_items)
    print(f"{GREEN} DOWNLOADING.... {RESET}")
    return success

def main():
    while True:
        clear_screen()
        show_header()

        # -----------------------------
        # Check FFmpeg
        # -----------------------------
        if not check_ffmpeg():

            title = "FFMPEG REQUIRED"

            content = (
                f"{RED}"
                "ffmpeg not found! Audio/MP3 conversion may not work."
                f"{RESET}"
            )

            linktoffmpeg = (
                f"{BLUE}"
                "Install ffmpeg: https://ffmpeg.org/download.html"
                f"{RESET}"
            )

            ansi_escape = re.compile(
                r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])'
            )

            def clean_len(text):
                return len(ansi_escape.sub('', text))

            content_width = max(
                clean_len(title),
                clean_len(linktoffmpeg),
                clean_len(content)
            ) + 4

            print(
                f"{GREEN}"
                f"╔{'═' * content_width}╗"
                f"{RESET}"
            )

            print(
                f"{GREEN}║"
                f"{title.center(content_width)}"
                f"║{RESET}"
            )

            print(
                f"{GREEN}║"
                f"{' ' * content_width}"
                f"║{RESET}"
            )

            print(
                f"{GREEN}║ {content}"
                f"{' ' * (content_width - clean_len(content) - 1)}"
                f"║{RESET}"
            )

            print(
                f"{GREEN}║ {linktoffmpeg}"
                f"{' ' * (content_width - clean_len(linktoffmpeg) - 1)}"
                f"║{RESET}"
            )

            print(
                f"{GREEN}"
                f"╚{'═' * content_width}╝"
                f"{RESET}"
            )

            print(
                f"\n{YELLOW}"
                "Please install FFmpeg and restart the program."
                f"{RESET}"
            )

            input(
                f"\n{GRAY}"
                "Press Enter to exit..."
                f"{RESET}"
            )

            sys.exit(1)

        # -----------------------------
        # Main Menu
        # -----------------------------
        show_menu()

        choice = input(
            f"{YELLOW}"
            "➜  Select an option [1-4]: "
            f"{RESET}"
        ).strip()

        # -----------------------------
        # Video Download
        # -----------------------------
        if choice == "1":

            clear_screen()
            show_header()

            urlInput()

            # urlInput()/process_url() should call pause()
            # when an error occurs.

        # -----------------------------
        # Audio Download
        # -----------------------------
        elif choice == "2":

            clear_screen()
            show_header()

            urlInput()

            # urlInput()/process_url() should call pause()
            # when an error occurs.

        # -----------------------------
        # About
        # -----------------------------
        elif choice == "3":

            clear_screen()
            show_header()

            about()

        # -----------------------------
        # Exit
        # -----------------------------
        elif choice == "4":

            clear_screen()
            thankyou()

            sys.exit(0)

        # -----------------------------
        # Invalid Choice
        # -----------------------------
        else:

            print(
                f"\n{RED}"
                "✘ Invalid option. Please choose 1-4."
                f"{RESET}"
            )

            time.sleep(1)


if __name__ == "__main__":
    main()
