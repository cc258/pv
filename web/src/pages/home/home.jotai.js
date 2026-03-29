import axios from 'axios';
import { atom } from "jotai";
export const homeVideo = atom([]);
export const getHomeVideoParams = atom({ page: 1, size: 8 });

export const getHomeVideo = atom(
  (get) => get(homeVideo), 
  async (get, set, params) => {
    const baseParams = get(getHomeVideoParams);
    const res = await axios.get('/api/video', {params: { ...baseParams, ...params }});

    const items = res.data?.data;
    if (Array.isArray(items)) {
      set(homeVideo, items);
    } else {
      console.error('Unexpected response:', res.data);
    }
  }
);