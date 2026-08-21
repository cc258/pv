import React, { useState, useEffect, useMemo, useRef } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAtomValue, useSetAtom } from 'jotai';

import { categoryVideo, categoryVideoMeta, getCategoryVideo } from './category.jotai.js';
import Categories from "../../components/categories/categories.jsx";

const PAGE_SIZE_OPTIONS = [10, 20];
const DEFAULT_PAGE_SIZE = 10;


function buildPageList(currentPage, totalPages) {
    const pages = [];
    if (totalPages <= 7) {
        for (let i = 1; i <= totalPages; i++) pages.push(i);
        return pages;
    }
    const left = Math.max(2, currentPage - 2);
    const right = Math.min(totalPages - 1, currentPage + 2);
    pages.push(1);
    if (left > 2) pages.push('…');
    for (let i = left; i <= right; i++) pages.push(i);
    if (right < totalPages - 1) pages.push('…');
    pages.push(totalPages);
    return pages;
}

const Category = () => {
    const navigate = useNavigate();
    const video = useAtomValue(categoryVideo);
    const videoMeta = useAtomValue(categoryVideoMeta);
    const setCategoryVideo = useSetAtom(getCategoryVideo);
    const [searchParams, setSearchParams] = useSearchParams();

    const category_id = searchParams.get('category_id');
    const category_name = searchParams.get('category_name');

    // URL 作为分页状态的唯一真源（single source of truth）——
    // 刷新 / 分享链接后仍能回到相同的分页位置。
    const pageParam = Number(searchParams.get('page'));
    const sizeParam = Number(searchParams.get('size'));
    const page = Number.isFinite(pageParam) && pageParam >= 1 ? pageParam : 1;
    const size = PAGE_SIZE_OPTIONS.includes(sizeParam) ? sizeParam : DEFAULT_PAGE_SIZE;

    const totalPages = Math.max(1, Math.ceil((videoMeta.total ?? 0) / size));
    const pageList = useMemo(() => buildPageList(page, totalPages), [page, totalPages]);

    // 本地 loading 占位（请求期间禁用翻页按钮，避免重复点击）
    const [loading, setLoading] = useState(false);

    const goTo = (nextPage, nextSize = size) => {
        const safePage = Math.min(Math.max(1, Number(nextPage) || 1), totalPages);
        const next = new URLSearchParams(searchParams);
        next.set('page', String(safePage));
        next.set('size', String(PAGE_SIZE_OPTIONS.includes(Number(nextSize)) ? Number(nextSize) : DEFAULT_PAGE_SIZE));
        // category_id / category_name 本来就在 searchParams 里，保留不动
        setSearchParams(next, { replace: false });
    };

    // 触发请求：URL 变化（或首屏）-> 拉新一页数据
    //   注意：setLoading 放到 queueMicrotask 是为了避免 React 19 的 eslint 规则
    //   "同步 setState 会触发级联渲染" —— 请求本身是异步的，我们只需要 UI 在下一帧显示 loading。
    useEffect(() => {
        if (!category_id) return;
        let cancelled = false;
        queueMicrotask(() => {
            if (!cancelled) setLoading(true);
        });
        Promise.resolve(setCategoryVideo({ category_id, page, size }))
            .finally(() => {
                if (!cancelled) setLoading(false);
            });
        return () => { cancelled = true; };
    }, [setCategoryVideo, category_id, page, size]);

    // category_id 改变：任何情况下都回到第 1 页（否则很容易落在新分类的越界空页）
    //   用 useRef 存上一次的值，而不是 useState——避免"在 useEffect 里同步 setState"触发的 cascading render eslint error。
    const prevCategoryIdRef = useRef(category_id);
    useEffect(() => {
        if (category_id !== prevCategoryIdRef.current) {
            prevCategoryIdRef.current = category_id;
            if (page !== 1) goTo(1, size);
        }
    }, [category_id, page, size]); // eslint-disable-line react-hooks/exhaustive-deps

    const renderVideo = () => {
        if (!video || video.length === 0) {
            return (
                <div className="col-span-full py-20 text-center text-gray-400">
                    <p className="text-lg">本分类暂时还没有视频</p>
                    <p className="mt-2 text-xs text-gray-500">可以换一个分类看看，或者稍后再回来</p>
                </div>
            );
        }
        return video.map((item) => {
            return (
                <div key={item.id ?? item.video_name}
                    className="relative group bg-[#1c1c1c] rounded overflow-hidden shadow hover:shadow-lg transition">
                    <img src={item.cover || 'https://cdn.myanimelist.net/images/anime/5/87048.jpg'} alt={item.video_name || item.name}
                        className="w-full h-52 object-cover group-hover:scale-105 transition-transform duration-300" />
                    <div
                        className="absolute inset-0 bg-black/70 flex items-center justify-center opacity-0 group-hover:opacity-100 transition duration-300">
                        <button onClick={() => navigate(`/play/${item.id}`)}
                            className="bg-green-600 px-4 py-2 rounded text-sm hover:bg-green-700">Watch Now
                        </button>
                    </div>
                    <div className="p-2">
                        <h3 className="text-sm font-semibold truncate" title={item.video_name}>{item.video_name}</h3>
                        <p className="text-xs text-gray-400 truncate" title={item.tags}>{item.tags}</p>
                    </div>
                </div>
            );
        });
    };

    const renderPagination = () => {
        if (totalPages <= 1 && !videoMeta.total) return null; // 还没加载到 meta 时不渲染
        const start = (videoMeta.total === 0) ? 0 : (page - 1) * size + 1;
        const end = Math.min(page * size, videoMeta.total ?? 0);

        return (
            <div className="mt-12 flex flex-col md:flex-row items-center justify-between gap-4 text-sm">
                {/* 左侧：当前范围统计 */}
                <div className="text-gray-400 whitespace-nowrap">
                    共 <span className="text-white font-medium">{videoMeta.total ?? 0}</span> 条，
                    当前 {start} - {end}
                </div>

                {/* 中间：页码按钮 */}
                <div className="flex items-center gap-2">
                    <button
                        type="button"
                        onClick={() => goTo(page - 1)}
                        disabled={page <= 1 || loading}
                        className="min-w-[36px] h-9 px-3 rounded border border-gray-700 bg-[#1c1c1c] text-gray-300
                                   disabled:opacity-40 disabled:cursor-not-allowed
                                   hover:border-green-500 hover:text-green-500 transition"
                    >上一页</button>

                    {pageList.map((p, idx) => {
                        if (p === '…') {
                            return (
                                <span key={`ellipsis-${idx}`}
                                    className="min-w-[36px] h-9 flex items-center justify-center text-gray-500">…</span>
                            );
                        }
                        const isActive = p === page;
                        return (
                            <button
                                key={p}
                                type="button"
                                onClick={() => goTo(p)}
                                disabled={loading}
                                className={
                                    'min-w-[36px] h-9 px-3 rounded border transition ' +
                                    (isActive
                                        ? 'bg-green-600 border-green-600 text-white hover:bg-green-700'
                                        : 'bg-[#1c1c1c] border-gray-700 text-gray-300 hover:border-green-500 hover:text-green-500') +
                                    ' disabled:opacity-40 disabled:cursor-not-allowed'
                                }
                            >{p}</button>
                        );
                    })}

                    <button
                        type="button"
                        onClick={() => goTo(page + 1)}
                        disabled={page >= totalPages || loading}
                        className="min-w-[36px] h-9 px-3 rounded border border-gray-700 bg-[#1c1c1c] text-gray-300
                                   disabled:opacity-40 disabled:cursor-not-allowed
                                   hover:border-green-500 hover:text-green-500 transition"
                    >下一页</button>
                </div>

                {/* 右侧：每页条数 + 跳转输入 */}
                <div className="flex items-center gap-3 text-gray-400">
                    <label className="flex items-center gap-2">
                        <span>每页</span>
                        <select
                            value={size}
                            onChange={(e) => {
                                // 每页数量改变 → 总页数会变，强制回到第 1 页防止越界空页
                                const newSize = Number(e.target.value);
                                goTo(1, newSize);
                            }}
                            className="h-9 px-2 rounded border border-gray-700 bg-[#1c1c1c] text-gray-200
                                       focus:outline-none focus:border-green-500 transition"
                        >
                            {PAGE_SIZE_OPTIONS.map((n) => (
                                <option key={n} value={n}>{n} 条</option>
                            ))}
                        </select>
                    </label>
                </div>
            </div>
        );
    };

    return (
        <div className="bg-[#0f0f0f] text-white font-sans min-h-screen flex flex-col">
            <header className="bg-[#1c1c1c] shadow-md">
                <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <button id="menu-btn" className="md:hidden text-white text-2xl">&#9776;</button>
                        <h1 onClick={() => navigate('/')} className="text-xl font-bold text-green-500 cursor-pointer">PV 朋友影视</h1>
                    </div>
                </div>
            </header>

            <Categories />

            <main className="flex-1">
                <section className="px-6 py-12 max-w-7xl mx-auto">
                    <h2 className="text-2xl font-bold mb-6 border-l-4 border-green-500 pl-3">
                        {category_name || (category_id ? `分类 #${category_id}` : '全部分类视频')}
                    </h2>

                    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                        {renderVideo()}
                    </div>

                    {/* 分页区 */}
                    {renderPagination()}

                    {loading && (
                        <div className="mt-6 text-center text-xs text-gray-500">加载中…</div>
                    )}
                </section>
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

export default Category;
