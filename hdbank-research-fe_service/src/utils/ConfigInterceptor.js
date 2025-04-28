import axios from "axios";


const http = axios.create({
    baseURL: "http://192.168.105.3:3000", //http://localhost:3200
})

http.interceptors.request.use((req) => {
        //req.headers = {... req.headers, 'ngrok-skip-browser-warning': true}
        return req; 
    }
     , (err) => 
        { 
            return Promise.reject(err) 
        });

http.interceptors.response.use((res) => { return res; }, (err) => { return Promise.reject(err) });

export default http;