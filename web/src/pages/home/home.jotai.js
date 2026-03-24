import axios from 'axios';
import { atom } from "jotai";

export const homeVideo = atom([]);
export const getHomeVideoParams = atom({ pageIndex: 1, pageSize: 8 });

export const getHomeVideo = atom((get) => get(homeVideo), async (get, set, params) => {
  const res = await axios.get('/api/video', {...getHomeVideoParams, ...params});

  if (Array.isArray(res.data.data)) {
    set(homeVideo, res.data.data);
  }
});
