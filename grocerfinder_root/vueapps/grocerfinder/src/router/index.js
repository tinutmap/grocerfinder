import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import ItemListView from '../views/ItemListView.vue'
import ItemDetailView from '../views/ItemDetailView.vue'
import CategoryListView from '../views/CategoryListView.vue'
import CategoryDetailView from '../views/CategoryDetailView.vue'
import NotFound404 from '../views/NotFound404.vue'
import HelloWorld from '../components/HelloWorld.vue'

const routes = [
  { path: '/login', component: Login },
  { path: '/', component: HelloWorld },
  { path: '/item', component: ItemListView },
  { path: '/item/:id', component: ItemDetailView },
  { path: '/category', component: CategoryListView },
  { path: '/category/:id', component: CategoryDetailView },
  { path: '/notFound404', name: 'notFound404', component: NotFound404 },
  // https://next.router.vuejs.org/guide/migration/#removed-star-or-catch-all-routes
  { path: '/:pathMatch(.*)*', name: 'notFound404', component: NotFound404 }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
