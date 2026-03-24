import React from 'react';
import { BrowserRouter } from 'react-router-dom';


import { Provider } from 'jotai';
import Routers from './routers';


const App = () => {
  return (
    <Provider>
      <BrowserRouter>
        <Routers />
      </BrowserRouter>
    </Provider>
  );
};
export default App;