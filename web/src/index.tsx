import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlay, faStepBackward, faStepForward, faPause } from '@fortawesome/free-solid-svg-icons'

library.add(faPlay, faStepBackward, faStepForward, faPause)

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

reportWebVitals();
