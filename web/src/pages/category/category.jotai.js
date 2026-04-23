import request from '../../utils/request';
import { atom } from "jotai";
export const categoryVideo = atom([]);

export const getCategoryVideo = atom(
  (get) => get(categoryVideo),
  async (get, set, params) => {
    const res = await request.get('/video', {params});

    const items = res.data;
    if (items) {
      set(categoryVideo, items);
    }
  }
);