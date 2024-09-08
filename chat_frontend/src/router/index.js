import { createRouter, createWebHistory } from 'vue-router';
import Layout from '../Layout.vue';
import Home from '../components/Home.vue';
import UserSpace from '../components/UserSpace.vue';
import Sign from '../components/Sign.vue';
import Signup from '../components/Signup.vue';
import Settings from '../components/Settings.vue';
import Chat from '../components/Chat.vue';
import KnowledgeGraph from '../components/KnowledgeGraph.vue';
import History from '../components/History.vue';

const routes = [
    {
      path: '/',
      redirect: '/base/home'
    },
    {
      path: '/api/login',
      component: Sign,
    },
    {
      path:'/api/register',
      component: Signup,
    },
    {
      path: '/base',
      component: Layout,
      children:[
        {
            path: 'home',
            component: Home,
        },
        {
            path: 'userspace',
            component: UserSpace
        },
        {
            path: 'settings',
            component: Settings
        },
        {
          path: 'chat',
          component: Chat
        },
        {
          path: 'kg',
          component: KnowledgeGraph
        },
        {
          path: 'history',
          component: History
        }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;