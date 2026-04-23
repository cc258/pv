import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAtomValue, useSetAtom } from 'jotai';

import { categoryVideo, getCategoryVideo } from './category.jotai.js';
import Categories from "../../components/categories/categories.jsx";

const Category = () => {
    const navigate = useNavigate();
    const video = useAtomValue(categoryVideo);      // 只读状态
    const setCategoryVideo = useSetAtom(getCategoryVideo); // 只写操作
    const [searchParams] = useSearchParams();
    const category_id = searchParams.get('category_id');
    const category_name = searchParams.get('category_name');

    useEffect(() => {
        setCategoryVideo({ category_id, page: 1, size: 24 });
    }, [setCategoryVideo]);

    const renderVideo = () => {
        return video.map((item, key) => {
            return <div key={key}
                className="relative group bg-[#1c1c1c] rounded overflow-hidden shadow hover:shadow-lg transition">
                <img src={item.cover || 'https://cdn.myanimelist.net/images/anime/5/87048.jpg'} alt={item.name}
                    className="w-full h-52 object-cover group-hover:scale-105 transition-transform duration-300" />
                <div
                    className="absolute inset-0 bg-black/70 flex items-center justify-center opacity-0 group-hover:opacity-100 transition duration-300">
                    <button onClick={() => navigate(`/play/${item.id}`)}
                        className="bg-green-600 px-4 py-2 rounded text-sm hover:bg-green-700">Watch Now
                    </button>
                </div>
                <div className="p-2">
                    <h3 className="text-sm font-semibold truncate">{item.video_name}</h3>
                    <p className="text-xs text-gray-400">{item.tags}</p>
                </div>
            </div>
        })
    }

    return (
        <div className="bg-[#0f0f0f] text-white font-sans">
            <header className="bg-[#1c1c1c] shadow-md">
                <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <button id="menu-btn" className="md:hidden text-white text-2xl">&#9776;</button>
                        <h1 onClick={() => navigate('/')} className="text-xl font-bold text-green-500">PV</h1>
                    </div>
                </div>
            </header>

            <Categories />

            <section className="px-6 py-12 max-w-7xl mx-auto">
                <h2 className="text-2xl font-bold mb-6 border-l-4 border-green-500 pl-3">{ category_name }</h2>

                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {renderVideo()}
                </div>
            </section>

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

export default Category;
