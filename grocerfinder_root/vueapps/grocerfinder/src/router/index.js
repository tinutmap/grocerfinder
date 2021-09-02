import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import ItemListView from '../views/ItemListView.vue'
import ItemById from '../views/ItemById.vue'
import CategoryListView from '../views/CategoryListView.vue'
import CategoryById from '../views/CategoryById.vue'
import NotFound404 from '../views/NotFound404.vue'

const routes = [
  { path: '/login', component: Login },
  { path: '/', redirect: '/item' },
  { path: '/item', component: ItemListView },
  { path: '/item/:id', component: ItemById },
  { path: '/category', component: CategoryListView },
  { path: '/category/:id', component: CategoryById },
  { path: '/notFound404', name: 'notFound404', component: NotFound404 },
  // https://next.router.vuejs.org/guide/migration/#removed-star-or-catch-all-routes
  { path: '/:pathMatch(.*)*', name: 'notFound404', component: NotFound404 }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
