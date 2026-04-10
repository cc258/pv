import request from '../../utils/request';
import { atom } from "jotai";
export const homeVideo = atom([]);
export const getHomeVideoParams = atom({ page: 1, size: 8 });

export const getHomeVideo = atom(
  (get) => get(homeVideo), 
  async (get, set, params) => {
    const baseParams = get(getHomeVideoParams);
    const res = await request.get('/video', {params: { ...baseParams, ...params }});

    const items = res.data;
    if (items) {
      set(homeVideo, items);
    }
  }
);