import request from '../../utils/request';
import { atom } from "jotai";

// 视频列表（当前页的数据集合）
export const categoryVideo = atom([]);

// 分页元数据：total 总数 / page 当前请求页码 / size 当前请求每页数量
export const categoryVideoMeta = atom({ total: 0, page: 1, size: 10 });

export const getCategoryVideo = atom(
  (get) => get(categoryVideo),
  async (get, set, params) => {
    const res = await request.get('/video', { params });

    // 后端 GET /video 返回 { data, total, page, size }
    const items = res?.data?.data;
    const total = res?.total ?? 0;
    const page = res?.page ?? params?.page ?? 1;
    const size = res?.size ?? params?.size ?? 10;

    if (Array.isArray(items)) {
      set(categoryVideo, items);
    } else if (Array.isArray(res?.data)) {
      // 兼容老接口（其他列表接口）直接返回数组的情况
      set(categoryVideo, res.data);
    }
    set(categoryVideoMeta, { total, page, size });
    console.log('total, page, size: ',total, page, size)
  }
);
