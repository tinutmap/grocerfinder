import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import AllItems from '../views/AllItems.vue'
import ItemById from '../views/ItemById.vue'
import CategoryAll from '../views/CategoryAll.vue'
import CategoryById from '../views/CategoryById.vue'
import NotFound404 from '@/NotFound404.vue'

const routes = [
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  { path: '/login', component: Login },
  { path: '/', redirect: '/item' },
  { path: '/item', component: AllItems },
  { path: '/item/:id', component: ItemById },
  { path: '/category', component: CategoryAll },
  { path: '/category/:id', component: CategoryById },
  { path: '/notFound404', name: 'notFound404', component: NotFound404 },
  { path: '*', component: NotFound404 }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
