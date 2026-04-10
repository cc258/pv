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
