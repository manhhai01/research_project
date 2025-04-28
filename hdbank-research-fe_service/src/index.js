import { createRoot } from 'react-dom/client';
import './assets/css/style.css'
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import App from './App';
import { Provider } from 'react-redux';
import { store } from './redux/configStore';

const root = createRoot(document.getElementById('root'));
root.render(
        <Provider store={store}>
                <App />
        </Provider>
);