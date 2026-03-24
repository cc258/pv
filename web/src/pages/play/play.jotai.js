import axios from 'axios';
import { atom } from "jotai";

export const video = atom({});
export const getVideoParams = atom({ pageIndex: 1, pageSize: 8 });

export const getVideo = atom((get) => get(video), async (get, set, id) => {
  const res = await axios.get(`/api/video/${id}`);

  if (res.data) {
    set(video, res.data);
  }
});
