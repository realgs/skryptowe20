import MainPage from "@/components/MainPage.vue";
import DataPanel from "@/components/DataPanel";
import Contact from "@/components/Contact";
import VueRouter from 'vue-router'
import Vue from 'vue'

Vue.use(VueRouter)

const routes = [
    {
        path: "/",
        name: "MainPage",
        component: MainPage,
    },
    {
        path: "/data-panel",
        name: "DataPanel",
        component: DataPanel,
    },
    {
        path: "/contact",
        name: "Contact",
        component: Contact,
    },

    
];

const router = new VueRouter({
 routes,
})

export default router;