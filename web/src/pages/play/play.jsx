import React, {useState, useEffect} from 'react';
import {useNavigate, useParams} from 'react-router-dom';
import {useAtom} from 'jotai';

import {getVideo, getTrendingVideo} from './play.jotai';
import Categories from "../../components/categories/categories.jsx";
import trailerSrc from '../../assets/film/trailer.mp4';

const Play = () => {
    const navigate = useNavigate();
    const {id} = useParams();
    const [video, setVideo] = useAtom(getVideo);
    const [trending, setTrending] = useAtom(getTrendingVideo);

    useEffect(() => {
        setVideo(id)
    }, [id])

    useEffect(() => {
        setTrending()
    }, [])


    return (
        <div className="bg-[#0f0f0f] text-white font-sans">
            <header className="bg-[#1c1c1c] shadow-md">
                <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <button id="menu-btn" className="md:hidden text-white text-2xl">&#9776;</button>
                        <h1 onClick={() => navigate('/')} className="text-xl font-bold text-green-500">PV 朋友影视</h1>
                    </div>
                </div>
            </header>

            <Categories />

            <main className="flex-grow max-w-7xl mx-auto px-4 py-10 grid grid-cols-1 md:grid-cols-3 gap-8">


                <section className="md:col-span-2 space-y-4">
                  <div className="w-full aspect-video bg-black rounded overflow-hidden shadow-lg relative">
                    <video
                      className="w-full h-full object-contain"
                      controls
                      controlsList="nodownload"
                      playsInline
                      preload="auto"
                      poster={video?.cover || "https://cdn.myanimelist.net/images/anime/10/47347.jpg"}
                      src={trailerSrc}
                    />
                  </div>

                  <div className="flex justify-between items-center text-green-400 font-semibold">
                    <span id="episode-info">{video?.video_name}</span>
                  </div>

                  <p className="text-xs text-gray-300 leading-relaxed">
                    {video?.tags}
                  </p>

                  <p className="text-gray-300 leading-relaxed">
                    {video?.comment}
                  </p>
                </section>


                <aside>
                    <h2 className="text-2xl font-bold mb-6 border-l-4 border-green-500 pl-3">Trending</h2>

                    <ul className="space-y-3">
                        {trending.map((item, index) => {
                            const rank = index + 1;
                            const rankColor = rank === 1
                                ? 'bg-yellow-500 text-black'
                                : rank === 2
                                    ? 'bg-gray-300 text-black'
                                    : rank === 3
                                        ? 'bg-amber-700 text-white'
                                        : 'bg-gray-700 text-gray-200';
                            return (
                                <li key={item.id}
                                    onClick={() => navigate(`/play/${item.id}`)}
                                    className="flex items-center gap-3 bg-[#1c1c1c] rounded overflow-hidden shadow hover:shadow-lg hover:bg-[#242424] transition cursor-pointer">
                                    <span className={`shrink-0 w-7 h-7 flex items-center justify-center text-xs font-bold ${rankColor}`}>
                                        {rank}
                                    </span>
                                    <img src={item.cover || 'https://cdn.myanimelist.net/images/anime/5/87048.jpg'}
                                         alt={item.video_name}
                                         className="w-16 h-20 object-cover"/>
                                    <div className="flex-1 min-w-0 pr-3 py-2">
                                        <h3 className="text-sm font-semibold truncate">{item.video_name}</h3>
                                        <p className="text-xs text-gray-400 truncate mt-1">{item.tags}</p>
                                    </div>
                                </li>
                            );
                        })}
                    </ul>
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
