import React, {useState, useEffect} from 'react';
import {useNavigate, useParams} from 'react-router-dom';
import {useAtom} from 'jotai';

import {getVideo} from './play.jotai';

const Play = () => {
    const navigate = useNavigate();
    const {id} = useParams();
    const [video, setVideo] = useAtom(getVideo);

    useEffect(() => {
        setVideo(id)
    }, [id])


    return (
        <div className="bg-[#0f0f0f] text-white font-sans">
            <header className="bg-[#1c1c1c] shadow-md">
                <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <button id="menu-btn" className="md:hidden text-white text-2xl">&#9776;</button>
                        <h1 onClick={() => navigate('/')} className="text-xl font-bold text-green-500">PV</h1>
                    </div>
                    {/* <nav className="hidden md:flex space-x-6 text-sm">
                        <a href="#" className="hover:text-green-400">Home</a>
                        <a href="#" className="hover:text-green-400">Trending</a>
                        <a href="#" className="hover:text-green-400">Genres</a>
                        <a href="#" className="hover:text-green-400">Movies</a>
                        <a href="#" className="hover:text-green-400">Login</a>
                    </nav> */}
                </div>
            </header>

            <div className="flex flex-wrap w-full p-6 gap-2 md:gap-2 items-center text-sm text-white md:text-md">

                <a href="#" className="bg-cyan-500 rounded px-2 py-1">
                    Copywriting
                </a>

                <a href="#" className="bg-cyan-500 rounded px-2 py-1">
                    Image
                    Generation
                </a>

                <a href="#" className="bg-cyan-500 rounded px-2 py-1">
                    Content
                    Creation
                </a>

                <a href="#" className="bg-cyan-500 rounded px-2 py-1">
                    Video
                    Generation
                </a>

                <a href="#" className="bg-cyan-500 rounded px-2 py-1">
                    Audio
                    Generation
                </a>

                <a href="#" className="bg-cyan-500 rounded px-2 py-1">
                    Design
                </a>

                <a href="#" className="bg-cyan-500 rounded px-2 py-1">
                    Photo
                    Editing
                </a>

                <a href="#" className="bg-cyan-500 rounded px-2 py-1">
                    Writing
                    Assistant
                </a>

                <a href="#" className="bg-cyan-500 rounded px-2 py-1">
                    Project
                    Management
                </a>

                <a href="#" className="bg-cyan-500 rounded px-2 py-1">
                    Video
                    Editing
                </a>
            </div>

            <main className="flex-grow max-w-7xl mx-auto px-4 py-10 grid grid-cols-1 md:grid-cols-3 gap-8">


                <section className="md:col-span-2 space-y-4">

                    <div className="w-full aspect-video bg-black rounded overflow-hidden shadow-lg">
                        <video
                            id="video-player"
                            className="w-full h-full bg-black"
                            controls
                            preload="metadata"
                            poster={video.cover || "https://cdn.myanimelist.net/images/anime/10/47347.jpg"}
                        >
                            <source src="https://media.w3.org/2010/05/sintel/trailer.mp4" type="video/mp4"/>
                            Your browser does not support the video tag.
                        </video>
                    </div>

                    <div className="flex justify-between items-center text-gray-400 text-sm font-semibold">
                        <button id="prev-ep"
                                className="px-3 py-1 rounded bg-green-700 hover:bg-green-800 disabled:opacity-50"
                                disabled>Previous Episode
                        </button>
                        <span id="episode-info" className="text-green-400">Episode 1 - {video.video_name}</span>
                        <button id="next-ep" className="px-3 py-1 rounded bg-green-700 hover:bg-green-800">Next Episode
                        </button>
                    </div>

                    <p className="text-gray-300 leading-relaxed">
                        Eren lives in a world where enormous walls protect humanity from man-eating giants known as
                        Titans. But when a colossal Titan breaks the wall, everything changes.
                    </p>

                </section>


                <aside>
                    <h2 className="text-2xl font-bold mb-6 border-l-4 border-green-500 pl-3">Trending Anime</h2>

                    <div className="grid grid-cols-2 sm:grid-cols-1 gap-4">

                        <div
                            className="relative group bg-[#1c1c1c] rounded overflow-hidden shadow hover:shadow-lg transition cursor-pointer"
                            onClick="loadAnime('Attack on Titan', 1, 'https://cdn.myanimelist.net/images/anime/10/47347.jpg', 'https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', 'Eren lives in a world where enormous walls protect humanity from man-eating giants known as Titans. But when a colossal Titan breaks the wall, everything changes.')">
                            <img src="https://cdn.myanimelist.net/images/anime/10/47347.jpg" alt="Attack on Titan"
                                 className="w-full h-32 object-cover group-hover:scale-105 transition-transform duration-300"/>
                            <div className="p-2">
                                <h3 className="text-sm font-semibold truncate">Attack on Titan</h3>
                                <p className="text-xs text-gray-400">24 eps • Action, Drama</p>
                            </div>
                            <span
                                className="absolute top-2 left-2 bg-green-600 text-white text-xs px-2 py-1 rounded">Ep 24</span>
                        </div>

                        <div
                            className="relative group bg-[#1c1c1c] rounded overflow-hidden shadow hover:shadow-lg transition cursor-pointer"
                            onClick="loadAnime('My Hero Academia', 1, 'https://cdn.myanimelist.net/images/anime/5/87048.jpg', 'https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4', 'A story about heroes with superpowers in a modern world.')">
                            <img src="https://cdn.myanimelist.net/images/anime/5/87048.jpg" alt="My Hero Academia"
                                 className="w-full h-32 object-cover group-hover:scale-105 transition-transform duration-300"/>
                            <div className="p-2">
                                <h3 className="text-sm font-semibold truncate">My Hero Academia</h3>
                                <p className="text-xs text-gray-400">13 eps • Super Power</p>
                            </div>
                            <span
                                className="absolute top-2 left-2 bg-green-600 text-white text-xs px-2 py-1 rounded">Ep 13</span>
                        </div>

                        <div
                            className="relative group bg-[#1c1c1c] rounded overflow-hidden shadow hover:shadow-lg transition cursor-pointer"
                            onClick="loadAnime('Death Note', 1, 'https://cdn.myanimelist.net/images/anime/4/19644.jpg', 'https://storage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4', 'A high schooler finds a notebook that can kill anyone whose name is written in it.')">
                            <img src="https://cdn.myanimelist.net/images/anime/4/19644.jpg" alt="Death Note"
                                 className="w-full h-32 object-cover group-hover:scale-105 transition-transform duration-300"/>
                            <div className="p-2">
                                <h3 className="text-sm font-semibold truncate">Death Note</h3>
                                <p className="text-xs text-gray-400">37 eps • Thriller, Supernatural</p>
                            </div>
                            <span
                                className="absolute top-2 left-2 bg-green-600 text-white text-xs px-2 py-1 rounded">Ep 37</span>
                        </div>

                    </div>
                </aside>
            </main>

            <footer className="bg-[#1c1c1c] border-t border-gray-700 py-8 mt-10 text-center text-sm text-gray-400">
                <div className="max-w-6xl mx-auto px-4">
                    <p>&copy; 2026 All rights reserved.</p>
                    <div className="mt-2 space-x-4">
                        <a href="#" className="hover:text-green-500">Terms</a>
                        <a href="#" className="hover:text-green-500">Privacy</a>
                        <a href="#" className="hover:text-green-500">Help</a>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Play;
