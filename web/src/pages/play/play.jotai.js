import request from '../../utils/request';
import { atom } from "jotai";

export const video = atom({});
export const getVideoParams = atom({ pageIndex: 1, pageSize: 8 });

export const getVideo = atom((get) => get(video), async (get, set, id) => {
  const res = await request.get(`/video/${id}`);

  if (res) {
    set(video, res);
  }
});

export const trendingVideo = atom([]);

export const getTrendingVideo = atom(
  (get) => get(trendingVideo),
  async (get, set, params) => {
    const res = await request.get('/video', { params: { sort: 'hot', size: 6, ...params } });

    const items = res.data;
    if (items) {
      set(trendingVideo, items);
    }
  }
);
