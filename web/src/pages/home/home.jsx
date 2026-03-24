import React, {useState, useEffect} from 'react';
import {useNavigate} from 'react-router-dom';
import {useAtom} from 'jotai';

import {getHomeVideo} from './home.jotai';

const Home = () => {
    const navigate = useNavigate();
    const [homeVideo, setHomeVideo] = useAtom(getHomeVideo);

    useEffect(() => {
        setHomeVideo()
    }, [])

    const renderHomeVideo = () => {
        return homeVideo.map((item, key) => {
            return <div key={key}
                        class="relative group bg-[#1c1c1c] rounded overflow-hidden shadow hover:shadow-lg transition">
                <img src={item.cover || 'https://cdn.myanimelist.net/images/anime/5/87048.jpg'} alt="Attack on Titan"
                     class="w-full h-52 object-cover group-hover:scale-105 transition-transform duration-300"/>
                <div
                    class="absolute inset-0 bg-black/70 flex items-center justify-center opacity-0 group-hover:opacity-100 transition duration-300">
                    <button onClick={() => navigate(`/play/${item.id}`)}
                            class="bg-green-600 px-4 py-2 rounded text-sm hover:bg-green-700">Watch Now
                    </button>
                </div>
                <div class="p-2">
                    <h3 class="text-sm font-semibold truncate">{item.video_name}</h3>
                    <p class="text-xs text-gray-400">24 eps • {item.tags}</p>
                </div>
                <span
                    class="absolute top-2 left-2 bg-green-600 text-white text-xs px-2 py-1 rounded">Ep 24</span>
            </div>
        })
    }

    return (
        <div class="bg-[#0f0f0f] text-white font-sans">
            <header class="bg-[#1c1c1c] shadow-md">
                <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <button id="menu-btn" class="md:hidden text-white text-2xl">&#9776;</button>
                        <h1 onClick={() => navigate('/')} class="text-xl font-bold text-green-500">PV</h1>
                    </div>
                    {/* <nav class="hidden md:flex space-x-6 text-sm">
                        <a href="#" class="hover:text-green-400">Home</a>
                        <a href="#" class="hover:text-green-400">Trending</a>
                        <a href="#" class="hover:text-green-400">Genres</a>
                        <a href="#" class="hover:text-green-400">Movies</a>
                        <a href="#" class="hover:text-green-400">Login</a>
                    </nav> */}
                </div>
            </header>

            <div class="flex flex-wrap w-full p-6 gap-2 md:gap-2 items-center text-sm text-white md:text-md">

                <a href="#" class="bg-cyan-500 rounded px-2 py-1">
                    Copywriting
                </a>

                <a href="#" class="bg-cyan-500 rounded px-2 py-1">
                    Image
                    Generation
                </a>

                <a href="#" class="bg-cyan-500 rounded px-2 py-1">
                    Content
                    Creation
                </a>

                <a href="#" class="bg-cyan-500 rounded px-2 py-1">
                    Video
                    Generation
                </a>

                <a href="#" class="bg-cyan-500 rounded px-2 py-1">
                    Audio
                    Generation
                </a>

                <a href="#" class="bg-cyan-500 rounded px-2 py-1">
                    Design
                </a>

                <a href="#" class="bg-cyan-500 rounded px-2 py-1">
                    Photo
                    Editing
                </a>

                <a href="#" class="bg-cyan-500 rounded px-2 py-1">
                    Writing
                    Assistant
                </a>

                <a href="#" class="bg-cyan-500 rounded px-2 py-1">
                    Project
                    Management
                </a>

                <a href="#" class="bg-cyan-500 rounded px-2 py-1">
                    Video
                    Editing
                </a>
            </div>

            <section class="px-6 py-12 max-w-7xl mx-auto">
                <h2 class="text-2xl font-bold mb-6 border-l-4 border-green-500 pl-3">Trending Anime</h2>

                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {renderHomeVideo()}
                </div>
            </section>

            <footer class="bg-[#1c1c1c] border-t border-gray-700 py-8 mt-10 text-center text-sm text-gray-400">
                <div class="max-w-6xl mx-auto px-4">
                    <p>&copy; 2026 All rights reserved.</p>
                    <div class="mt-2 space-x-4">
                        <a href="#" class="hover:text-green-500">Terms</a>
                        <a href="#" class="hover:text-green-500">Privacy</a>
                        <a href="#" class="hover:text-green-500">Help</a>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Home;
