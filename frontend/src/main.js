import { createApp } from 'vue';
import App from './App.vue';
import {createRouter, createWebHistory} from "vue-router";
import './assets/tailwind.css'
import LandingPage from "@/view/LandingPage/LandingPage.vue";
import UploadPage from "@/view/UploadPage/UploadPage.vue";
import Cors from "cors";
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';
import store from "./store";

const router = createRouter({
    history: createWebHistory(),
    routes: [ {
            path:"/",
            name:'Home',
            component: LandingPage
        },
        {
            path:"/upload",
            name: 'Upload',
            component: UploadPage
        }
    ]
});

createApp(App)
    .use(store)
    .use(VueDatePicker)
    .use(router)
    .use(Cors)
    .mount('#app')
