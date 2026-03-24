import React, { lazy } from 'react';
import { Navigate, useRoutes } from 'react-router-dom';

const Home = lazy(() => import('./pages/home/home'));
const Play = lazy(() => import('./pages/play/play'));

export const PATH = {
  MAIN: '/',
  HOME: '/home',
  PLAY: '/play/:id',
};

export const ROUTERS = [
  {
    path: PATH.MAIN,
    element: <Home />,
    title: 'HOME',
    nav: true,
  },
  {
    path: PATH.PLAY,
    element: <Play />,
    title: 'PLAY',
    nav: true,
  },
  {
    path: PATH.HOME,
    element: <Home />,
    title: 'HOME',
    nav: true,
  },
  {
    path: '*',
    element: <Navigate to={PATH.HOME} replace />,
  },
];

const Routers = () => {
  return useRoutes(ROUTERS);
};

export default Routers;
