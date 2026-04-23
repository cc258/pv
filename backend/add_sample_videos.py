#!/usr/bin/env python3
"""
添加示例视频数据到数据库
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session
from backend.app.core.deps import engine
from backend.app.models.videos import Video, Category, VideoCategory
from sqlmodel import select

VIDEOS = [
    # Drama
    {"video_name": "The Shawshank Redemption", "year": 1994, "cover": "https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljX漏概@._V1_.jpg", "tags": "Drama", "comment": "Hope is a good thing", "stars": 5, "categories": ["Drama"]},
    {"video_name": "The Godfather", "year": 1972, "cover": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGc@._V1_.jpg", "tags": "Drama, Crime", "comment": "An offer you can't refuse", "stars": 5, "categories": ["Drama", "Crime"]},
    {"video_name": "Forrest Gump", "year": 1994, "cover": "https://m.media-amazon.com/images/M/MV5BNDYwNzVjMTItZmU5YS00YjQ5LTljYjgtMjY2NDVmYWMyNWFmXkEyXkFqcGc@._V1_.jpg", "tags": "Drama, Romance, Comedy", "comment": "Life is like a box of chocolates", "stars": 5, "categories": ["Drama", "Romance", "Comedy"]},
    {"video_name": "Schindler's List", "year": 1993, "cover": "https://m.media-amazon.com/images/M/MV5BNDE4OTMxMTctNmRhYy00NWE2LTg3YzItYTk3M2UwOTU5Njg4XkEyXkFqcGc@._V1_.jpg", "tags": "Drama, History", "comment": "Whoever saves one life saves the world entire", "stars": 5, "categories": ["Drama"]},
    {"video_name": "12 Angry Men", "year": 1957, "cover": "https://m.media-amazon.com/images/M/MV5BM2U1NGZjYzktZmI2MS00NjFjLTk3YjctNGE1NGFkYjY5Y2JkXkEyXkFqcGc@._V1_.jpg", "tags": "Drama", "comment": "Juror #8 changed everything", "stars": 5, "categories": ["Drama"]},
    {"video_name": "Farewell My Concubine", "year": 1993, "cover": "https://m.media-amazon.com/images/M/MV5BNTMxNTMyODk4NV5BMl5BanBnXkFtZTcwMjI1MDk1NA@@._V1_.jpg", "tags": "Drama, Romance", "comment": "Better to be a devil than to be a ghost", "stars": 5, "categories": ["Drama", "Romance"]},
    {"video_name": "Life is Beautiful", "year": 1997, "cover": "https://m.media-amazon.com/images/M/MV5BYmJmM2Q4NmMtYThmNS00MzQ5LWFmHWYtMDVkNWU2ZjU1NTFiXkEyXkFqcGc@._V1_.jpg", "tags": "Drama, Comedy, Romance", "comment": "This is a simple story but not ordinary", "stars": 5, "categories": ["Drama", "Comedy", "Romance"]},
    {"video_name": "The Great Dictator", "year": 1940, "cover": "https://m.media-amazon.com/images/M/MV5BMTU1OTg0NTg5NF5BMl5BanBnXkFtZTcwMDY2NTk2Mw@@._V1_.jpg", "tags": "Drama, Comedy", "comment": "I'm sorry but I don't want to be an emperor", "stars": 5, "categories": ["Drama", "Comedy"]},

    # Romance
    {"video_name": "Titanic", "year": 1997, "cover": "https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E2My00Zjc5LWFjN2YtM2M4NzAzNmEyNDJhXkEyXkFqcGc@._V1_.jpg", "tags": "Romance, Drama", "comment": "I'll never let go", "stars": 5, "categories": ["Romance", "Drama"]},
    {"video_name": "Gone with the Wind", "year": 1939, "cover": "https://m.media-amazon.com/images/M/MV5BMjYwOGQ1ZDgtMTU3Ny00NTdkLWFmNDAtMDI3MjFjNzBmOTA5XkEyXkFqcGc@._V1_.jpg", "tags": "Romance, Drama", "comment": "After all... tomorrow is another day", "stars": 5, "categories": ["Romance", "Drama"]},
    {"video_name": "Roman Holiday", "year": 1953, "cover": "https://m.media-amazon.com/images/M/MV5BMDQwMzQ5NGEtNjkxZS00MzFiLWI1NzAtNmY1NmE4NjhkMmE0XkEyXkFqcGc@._V1_.jpg", "tags": "Romance, Comedy", "comment": "Seeds of love in ancient Rome", "stars": 5, "categories": ["Romance", "Comedy"]},
    {"video_name": "Pride and Prejudice", "year": 2005, "cover": "https://m.media-amazon.com/images/M/MV5BMTA1NDQ0MTY4MzZeQTJeQWpwZ15BbWU3MDEyNDI1ODk3XkEyXkFqcGc@._V1_.jpg", "tags": "Romance, Drama", "comment": "Only you have bewitched me", "stars": 5, "categories": ["Romance", "Drama"]},
    {"video_name": "The Notebook", "year": 2004, "cover": "https://m.media-amazon.com/images/M/MV5BMTk3OTM5Njg5M15BMl5BanBnXkFtZTYwMzA0ODI3._V1_.jpg", "tags": "Romance, Drama", "comment": "Our story is worth telling again", "stars": 5, "categories": ["Romance", "Drama"]},
    {"video_name": "Love Actually", "year": 2003, "cover": "https://m.media-amazon.com/images/M/MV5BMTY4NjQ5NDc0Nl5BMl5BanBnXkFtZTYwNjk5NDM3._V1_.jpg", "tags": "Romance, Comedy", "comment": "Love is actually all around", "stars": 5, "categories": ["Romance", "Comedy"]},

    # Horror
    {"video_name": "The Shining", "year": 1980, "cover": "https://m.media-amazon.com/images/M/MV5BZTkwZjUyOTAtZTQ0Mi00MGIyLWFjNWItYjU1MDcyMGFiZTMwXkEyXkFqcGc@._V1_.jpg", "tags": "Horror, Drama", "comment": "Here's Johnny!", "stars": 5, "categories": ["Horror", "Drama"]},
    {"video_name": "Psycho", "year": 1960, "cover": "https://m.media-amazon.com/images/M/MV5BNTQwNDM1YzItNDAxZC00NWY2LTk0M2UtNDIwNWI5OGUyNWUxXkEyXkFqcGc@._V1_.jpg", "tags": "Horror, Mystery", "comment": "Mother, what a movie", "stars": 5, "categories": ["Horror"]},
    {"video_name": "The Exorcist", "year": 1973, "cover": "https://m.media-amazon.com/images/M/MV5BYjhmMGMxZDYtMTkyNy00YWVmLTgyYmUtYTU3ZjcwNTBjN2I1XkEyXkFqcGc@._V1_.jpg", "tags": "Horror", "comment": "The power of Christ compels you", "stars": 5, "categories": ["Horror"]},
    {"video_name": "Silence of the Lambs", "year": 1991, "cover": "https://m.media-amazon.com/images/M/MV5BNjNhZTk0ZmEtNjA0NS00NDc5LTg1OGUtOTBlNWI0ZjhiNWI4XkEyXkFqcGc@._V1_.jpg", "tags": "Horror, Crime, Thriller", "comment": "I ate his liver with some fava beans", "stars": 5, "categories": ["Horror", "Crime"]},
    {"video_name": "A Nightmare on Elm Street", "year": 1984, "cover": "https://m.media-amazon.com/images/M/MV5BN2FjNWRkOWQtMGE2MS00NzY2LWE2ZmYtMDFhM2RjNjM1YjJiXkEyXkFqcGc@._V1_.jpg", "tags": "Horror", "comment": "A whole new kind of nightmare", "stars": 4, "categories": ["Horror"]},

    # Action
    {"video_name": "The Dark Knight", "year": 2008, "cover": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg", "tags": "Action, Crime, Drama", "comment": "Why so serious?", "stars": 5, "categories": ["Action", "Crime", "Drama"]},
    {"video_name": "Gladiator", "year": 2000, "cover": "https://m.media-amazon.com/images/M/MV5BMDliMm1kM2MtYzM1Mi00ZjkxLTk1MDEtYzA4MGU5N2JhOTlhXkEyXkFqcGc@._V1_.jpg", "tags": "Action, Drama", "comment": "Are you not entertained?", "stars": 5, "categories": ["Action", "Drama"]},
    {"video_name": "Inception", "year": 2010, "cover": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg", "tags": "Action, Sci-Fi, Thriller", "comment": "Your mind is the scene of the crime", "stars": 5, "categories": ["Action", "Sci-Fi", "Thriller"]},
    {"video_name": "The Matrix", "year": 1999, "cover": "https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZTY0ODQyNDRhXkEyXkFqcGc@._V1_.jpg", "tags": "Action, Sci-Fi", "comment": "There is no spoon", "stars": 5, "categories": ["Action", "Sci-Fi"]},
    {"video_name": "Mad Max: Fury Road", "year": 2015, "cover": "https://m.media-amazon.com/images/M/MV5BN2EwM2I5OWMtMGQyMi00Zjg1LWJkNTctZTdjYTA4OGUwZjMyXkEyXkFqcGc@._V1_.jpg", "tags": "Action, Adventure", "comment": "What a lovely day", "stars": 5, "categories": ["Action"]},
    {"video_name": "John Wick", "year": 2014, "cover": "https://m.media-amazon.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_.jpg", "tags": "Action, Crime", "comment": "He killed the wrong dog", "stars": 5, "categories": ["Action", "Crime"]},
    {"video_name": "Die Hard", "year": 1988, "cover": "https://m.media-amazon.com/images/M/MV5BNzQxUTE0MjktY2I0Mi00ODcyLWFjNTctMTZhMmRlMDIxZmE5XkEyXkFqcGc@._V1_.jpg", "tags": "Action, Thriller", "comment": "Yippee-ki-yay", "stars": 5, "categories": ["Action", "Thriller"]},

    # Sci-Fi
    {"video_name": "Interstellar", "year": 2014, "cover": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGc@._V1_.jpg", "tags": "Sci-Fi, Adventure, Drama", "comment": "Love is the only thing that transcends dimensions", "stars": 5, "categories": ["Sci-Fi", "Drama"]},
    {"video_name": "2001: A Space Odyssey", "year": 1968, "cover": "https://m.media-amazon.com/images/M/MV5BMmNlODY5NzYtMzAwMi00NjFkLTk2MGEtZDk1ZmM2NDE1NzExXkEyXkFqcGc@._V1_.jpg", "tags": "Sci-Fi, Mystery", "comment": "Open the pod bay doors, HAL", "stars": 5, "categories": ["Sci-Fi"]},
    {"video_name": "Blade Runner", "year": 1982, "cover": "https://m.media-amazon.com/images/M/MV5BNzQzMzJhZGEtNDgwNS00MmMyLTkyYjktOTUyNzAtYjU4N2MyMTMyYmU2XkEyXkFqcGc@._V1_.jpg", "tags": "Sci-Fi, Drama, Thriller", "comment": "All those moments will be lost in time", "stars": 5, "categories": ["Sci-Fi", "Drama", "Thriller"]},
    {"video_name": "The Terminator", "year": 1984, "cover": "https://m.media-amazon.com/images/M/MV5BNmZlYjViMjEtMmM2Mi00NmRkLWIyYWUtYWMyTBAZGZmOGY1XkEyXkFqcGc@._V1_.jpg", "tags": "Sci-Fi, Action", "comment": "I'll be back", "stars": 5, "categories": ["Sci-Fi", "Action"]},
    {"video_name": "Back to the Future", "year": 1985, "cover": "https://m.media-amazon.com/images/M/MV5BnmY2M5MGMtMmQxMi00ZTQ4LTg2N2YtNDg4NDI3ODBmY2M5XkEyXkFqcGc@._V1_.jpg", "tags": "Sci-Fi, Adventure, Comedy", "comment": "Where we're going, we don't need roads", "stars": 5, "categories": ["Sci-Fi", "Comedy", "Adventure"]},
    {"video_name": "The Martian", "year": 2015, "cover": "https://m.media-amazon.com/images/M/MV5BMTc2MTQ3MjQ1NV5BMl5BanBnXkFtZTgwMzk1MzEzNTE@._V1_.jpg", "tags": "Sci-Fi, Adventure, Comedy", "comment": "I'm gonna have to science the shit out of this", "stars": 5, "categories": ["Sci-Fi", "Comedy"]},

    # Comedy
    {"video_name": "The Grand Budapest Hotel", "year": 2014, "cover": "https://m.media-amazon.com/images/M/MV5BMzM5NjUxOTEyMl5BMl5BanBnXkFtZTgwNjEyMDM0MDE@._V1_.jpg", "tags": "Comedy, Drama", "comment": "A Wes Anderson masterpiece", "stars": 5, "categories": ["Comedy", "Drama"]},
    {"video_name": "The Hangover", "year": 2009, "cover": "https://m.media-amazon.com/images/M/MV5BNGQwZjg5YmYtY2IwNC00NjA3LWFjYTctNDcwM2JkNTM0OGNmXkEyXkFqcGc@._V1_.jpg", "tags": "Comedy", "comment": "What happens in Vegas stays in Vegas", "stars": 4, "categories": ["Comedy"]},
    {"video_name": "Superbad", "year": 2007, "cover": "https://m.media-amazon.com/images/M/MV5BMTc0NjIyMjA2OF5BMl5BanBnXkFtZTcwMzIxNDE1MQ@@._V1_.jpg", "tags": "Comedy", "comment": "The best summer of our lives", "stars": 4, "categories": ["Comedy"]},
    {"video_name": "Pulp Fiction", "year": 1994, "cover": "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTUxLWI5ZGYtYWYwYWZlNjgyYjMyXkEyXkFqcGc@._V1_.jpg", "tags": "Comedy, Crime, Drama", "comment": "Say what again", "stars": 5, "categories": ["Comedy", "Crime", "Drama"]},
    {"video_name": "Monty Python and the Holy Grail", "year": 1975, "cover": "https://m.media-amazon.com/images/M/MV5BNDQ2MzE1OTUtNDQ5Ny00ZGMzLThiOTgtN2ZkYjVjODEzZjUzXkEyXkFqcGc@._V1_.jpg", "tags": "Comedy, Adventure", "comment": "Your mother was a hamster", "stars": 5, "categories": ["Comedy"]},

    # Animation
    {"video_name": "Spirited Away", "year": 2001, "cover": "https://m.media-amazon.com/images/M/MV5BMjlmZmI5MDctNDE2YS00YWEwLWE5ZWItZDBhYWQ0NTcxNWRhXkEyXkFqcGc@._V1_.jpg", "tags": "Animation, Adventure, Family", "comment": "Once you meet someone, you never really forget them", "stars": 5, "categories": ["Animation"]},
    {"video_name": "WALL-E", "year": 2008, "cover": "https://m.media-amazon.com/images/M/MV5BMjExMTg5OTU0NF5BMl5BanBnXkFtZTcwMjMxMzMzMw@@._V1_.jpg", "tags": "Animation, Adventure, Family", "comment": "The cutest love story ever told", "stars": 5, "categories": ["Animation", "Comedy", "Adventure"]},
    {"video_name": "Up", "year": 2009, "cover": "https://m.media-amazon.com/images/M/MV5BMTk1NDIzODc5NF5BMl5BanBnXkFtZTcwMzA0MTMzMw@@._V1_.jpg", "tags": "Animation, Adventure, Comedy", "comment": "Adventure is out there", "stars": 5, "categories": ["Animation", "Comedy", "Adventure"]},
    {"video_name": "Toy Story", "year": 1995, "cover": "https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGc@._V1_.jpg", "tags": "Animation, Adventure, Comedy", "comment": "To infinity and beyond", "stars": 5, "categories": ["Animation", "Comedy", "Adventure"]},
    {"video_name": "Your Name", "year": 2016, "cover": "https://m.media-amazon.com/images/M/MV5BODI1YjU2MGYtNTIzNS00YTVkLTk2MGYtMWFlMWU5ZWMzNWQ4XkEyXkFqcGc@._V1_.jpg", "tags": "Animation, Drama, Romance", "comment": "We were meant to meet", "stars": 5, "categories": ["Animation", "Romance"]},
    {"video_name": "Demon Slayer: Mugen Train", "year": 2020, "cover": "https://m.media-amazon.com/images/M/MV5BNzU4YWE5MDMtN2JhNi00NjEyLTg1NmUtNGNmYjA5NWI4NWE5XkEyXkFqcGc@._V1_.jpg", "tags": "Animation, Action, Adventure", "comment": "Fortune cuels those who stay on their path", "stars": 5, "categories": ["Animation", "Action"]},

    # Thriller
    {"video_name": "Se7en", "year": 1995, "cover": "https://m.media-amazon.com/images/M/MV5BY2IzNzMxZjctZjUxZi00YzAxLTk3ZjMtODFjODdhMDU5N2M3XkEyXkFqcGc@._V1_.jpg", "tags": "Thriller, Crime, Drama", "comment": "Seven deadly sins", "stars": 5, "categories": ["Thriller", "Crime"]},
    {"video_name": "Fight Club", "year": 1999, "cover": "https://m.media-amazon.com/images/M/MV5BOTgyOGQ1NDItNGU3Ny00MjU3LTg2YWEtNmEyYjBiMjI1Y2M5XkEyXkFqcGc@._V1_.jpg", "tags": "Thriller, Drama", "comment": "The first rule of Fight Club is...", "stars": 5, "categories": ["Thriller", "Drama"]},
    {"video_name": "Zodiac", "year": 2007, "cover": "https://m.media-amazon.com/images/M/MV5BMTg5Mzk4MzQ0OV5BMl5BanBnXkFtZTcwNDQ0NTE3MQ@@._V1_.jpg", "tags": "Thriller, Crime, Mystery", "comment": "There is nothing more terrifying than a serial killer who knows your name", "stars": 5, "categories": ["Thriller", "Crime"]},

    # Crime
    {"video_name": "Goodfellas", "year": 1990, "cover": "https://m.media-amazon.com/images/M/MV5BY2NkZjEzMDgtN2RjYy00YzM1LWI4ZmQtMjIwYjFjNmI3ZGEwXkEyXkFqcGc@._V1_.jpg", "tags": "Crime, Drama", "comment": "Funny how?", "stars": 5, "categories": ["Crime", "Drama"]},
    {"video_name": "The Departed", "year": 2006, "cover": "https://m.media-amazon.com/images/M/MV5BMTI1MTY2OTIxNV5BMl5BanBnXkFtZTYwNjQ5Njg3._V1_.jpg", "tags": "Crime, Drama, Thriller", "comment": "I'm the guy who does his job. You are not.", "stars": 5, "categories": ["Crime", "Drama", "Thriller"]},
    {"video_name": "No Country for Old Men", "year": 2007, "cover": "https://m.media-amazon.com/images/M/MV5BMjA5Nzk1NjQ4OV5BMl5BanBnXkFtZTcwOTc3MDUzMQ@@._V1_.jpg", "tags": "Crime, Drama, Thriller", "comment": "If you hold to this you are a lucky man", "stars": 5, "categories": ["Crime", "Drama", "Thriller"]},
]


def add_sample_videos():
    with Session(engine) as session:
        categories = session.exec(select(Category)).all()
        cat_map = {c.name: c for c in categories}
        print(f"Found categories: {list(cat_map.keys())}")

        added_count = 0
        for video_data in VIDEOS:
            existing = session.exec(
                select(Video).where(Video.video_name == video_data["video_name"])
            ).first()
            if existing:
                continue

            cat_names = video_data.pop("categories", [])
            video = Video(**video_data)
            session.add(video)
            session.commit()
            session.refresh(video)

            for cat_name in cat_names:
                if cat_name in cat_map:
                    vc = VideoCategory(video_id=video.id, category_id=cat_map[cat_name].id)
                    session.add(vc)

            session.commit()
            print(f"Added: {video_data['video_name']} -> {cat_names}")
            added_count += 1

        print(f"\nTotal added: {added_count} videos")


if __name__ == "__main__":
    add_sample_videos()
