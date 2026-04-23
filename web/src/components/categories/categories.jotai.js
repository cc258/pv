import request from '../../utils/request';
import { atom } from "jotai";

export const categories = atom([]);

export const getCategories = atom((get) => get(categories), async (get, set, id) => {
  const res = await request.get(`/categories`);

  if (res) {
    set(categories, res);
  }
});
